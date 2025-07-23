/**
 * Cloudflare Worker for Automated Article Generation
 * Runs the Python article generator on schedule and webhook triggers
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Handle different endpoints
    switch (url.pathname) {
      case '/generate':
        return await handleGenerate(request, env);
      case '/health':
        return new Response('OK', { status: 200 });
      case '/webhook':
        return await handleWebhook(request, env);
      default:
        return new Response('Not Found', { status: 404 });
    }
  },

  async scheduled(event, env, ctx) {
    // Daily scheduled execution
    console.log('Running scheduled article generation');
    return await executeArticleGeneration(env);
  }
};

async function handleGenerate(request, env) {
  try {
    // Authenticate request
    const authHeader = request.headers.get('Authorization');
    if (!authHeader || authHeader !== `Bearer ${env.API_SECRET}`) {
      return new Response('Unauthorized', { status: 401 });
    }

    const result = await executeArticleGeneration(env);
    return new Response(JSON.stringify(result), {
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error) {
    console.error('Generation error:', error);
    return new Response(JSON.stringify({ 
      success: false, 
      error: error.message 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

async function handleWebhook(request, env) {
  try {
    // Verify GitHub webhook signature
    const signature = request.headers.get('X-Hub-Signature-256');
    const payload = await request.text();
    
    if (!verifyGitHubSignature(payload, signature, env.GITHUB_WEBHOOK_SECRET)) {
      return new Response('Invalid signature', { status: 401 });
    }

    const data = JSON.parse(payload);
    
    // Trigger generation on specific events
    if (data.action === 'generate_article' || data.ref === 'refs/heads/main') {
      const result = await executeArticleGeneration(env);
      return new Response(JSON.stringify(result), {
        headers: { 'Content-Type': 'application/json' }
      });
    }

    return new Response('OK', { status: 200 });
  } catch (error) {
    console.error('Webhook error:', error);
    return new Response('Internal Server Error', { status: 500 });
  }
}

async function executeArticleGeneration(env) {
  try {
    console.log('Starting article generation process');
    
    // Validate required secrets
    if (!env.GEMINI_API_KEYS) {
      throw new Error('GEMINI_API_KEYS secret not configured');
    }
    if (!env.GITHUB_TOKEN) {
      throw new Error('GITHUB_TOKEN secret not configured');
    }
    if (!env.GITHUB_REPO) {
      throw new Error('GITHUB_REPO not configured');
    }
    
    // Prepare configuration for Python script
    const config = {
      GEMINI_API_KEYS: env.GEMINI_API_KEYS,
      GITHUB_TOKEN: env.GITHUB_TOKEN,
      GITHUB_REPO: env.GITHUB_REPO,
      GITHUB_BRANCH: env.GITHUB_BRANCH || 'main',
      BLOG_CONFIG: JSON.stringify({
        category: 'Interior Design',
        author: 'Admin',
        max_daily_articles: 2
      }),
      // Keywords will be read from keyword.txt file, but provide fallback
      BLOG_KEYWORDS: env.BLOG_KEYWORDS || JSON.stringify([
        "modern living room design",
        "contemporary kitchen ideas", 
        "bedroom decoration tips",
        "bathroom renovation guide",
        "home office setup",
        "minimalist interior design"
      ]),
      UNSPLASH_ACCESS_KEY: env.UNSPLASH_ACCESS_KEY || '',
      PIXEL_API_CONFIG: env.PIXEL_API_CONFIG || '[]',
      ARTICLES_DATA: await getArticlesData(env)
    };

    console.log('Configuration prepared, triggering GitHub workflow...');
    
    // Execute Python script via GitHub Actions API
    const workflowResult = await triggerGitHubWorkflow(env, config);
    
    if (workflowResult.success) {
      // Update stored articles data
      await updateArticlesData(env, workflowResult.data);
      console.log('Article generation completed successfully');
    }

    return workflowResult;
  } catch (error) {
    console.error('Execution error:', error);
    return {
      success: false,
      message: `Execution failed: ${error.message}`,
      timestamp: new Date().toISOString()
    };
  }
}

async function triggerGitHubWorkflow(env, config) {
  try {
    const workflowUrl = `https://api.github.com/repos/${env.GITHUB_REPO}/actions/workflows/generate-article.yml/dispatches`;
    
    const response = await fetch(workflowUrl, {
      method: 'POST',
      headers: {
        'Authorization': `token ${env.GITHUB_TOKEN}`,
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ref: env.GITHUB_BRANCH || 'main',
        inputs: {
          config_data: JSON.stringify(config)
        }
      })
    });

    if (response.ok) {
      console.log('GitHub workflow triggered successfully');
      return {
        success: true,
        message: 'Article generation workflow triggered',
        workflow_id: await getLatestWorkflowRun(env),
        timestamp: new Date().toISOString()
      };
    } else {
      const errorText = await response.text();
      throw new Error(`GitHub API error: ${response.status} - ${errorText}`);
    }
  } catch (error) {
    console.error('GitHub workflow trigger error:', error);
    return {
      success: false,
      message: `Workflow trigger failed: ${error.message}`,
      timestamp: new Date().toISOString()
    };
  }
}

async function getLatestWorkflowRun(env) {
  try {
    const runsUrl = `https://api.github.com/repos/${env.GITHUB_REPO}/actions/workflows/generate-article.yml/runs?per_page=1`;
    
    const response = await fetch(runsUrl, {
      headers: {
        'Authorization': `token ${env.GITHUB_TOKEN}`,
        'Accept': 'application/vnd.github.v3+json'
      }
    });

    if (response.ok) {
      const data = await response.json();
      return data.workflow_runs[0]?.id || null;
    }
  } catch (error) {
    console.error('Error getting workflow run:', error);
  }
  return null;
}

async function getArticlesData(env) {
  try {
    // Try to get from KV storage first
    const stored = await env.ARTICLES_KV?.get('articles_data');
    if (stored) {
      return stored;
    }

    // Fallback to GitHub API to get existing articles
    const response = await fetch(`https://api.github.com/repos/${env.GITHUB_REPO}/contents/_posts`, {
      headers: {
        'Authorization': `token ${env.GITHUB_TOKEN}`,
        'Accept': 'application/vnd.github.v3+json'
      }
    });

    if (response.ok) {
      const files = await response.json();
      const articles = files.filter(file => file.name.endsWith('.md')).map(file => ({
        title: file.name.replace(/^\d{4}-\d{2}-\d{2}-/, '').replace('.md', ''),
        created_at: file.name.substring(0, 10),
        filename: file.name
      }));

      const articlesData = {
        articles: articles,
        used_keywords: [],
        daily_requests: 0,
        last_updated: new Date().toISOString()
      };

      return JSON.stringify(articlesData);
    }
  } catch (error) {
    console.error('Error getting articles data:', error);
  }

  return JSON.stringify({ articles: [], used_keywords: [], daily_requests: 0 });
}

async function updateArticlesData(env, newData) {
  try {
    if (env.ARTICLES_KV && newData) {
      await env.ARTICLES_KV.put('articles_data', JSON.stringify(newData));
      console.log('Articles data updated in KV storage');
    }
  } catch (error) {
    console.error('Error updating articles data:', error);
  }
}

function verifyGitHubSignature(payload, signature, secret) {
  if (!signature || !secret) return false;
  
  const encoder = new TextEncoder();
  const data = encoder.encode(payload);
  const key = encoder.encode(secret);
  
  return crypto.subtle.importKey(
    'raw',
    key,
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  ).then(cryptoKey => {
    return crypto.subtle.sign('HMAC', cryptoKey, data);
  }).then(signatureBuffer => {
    const expectedSignature = 'sha256=' + Array.from(new Uint8Array(signatureBuffer))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
    return expectedSignature === signature;
  }).catch(() => false);
}