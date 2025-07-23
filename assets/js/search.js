document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  const searchForm = document.querySelector('form[role="search"]');
  let searchIndex = [];
  
  // Get the correct base URL for multi-domain support
  function getBaseUrl() {
    const metaBaseUrl = document.querySelector('meta[name="base-url"]');
    if (metaBaseUrl) {
      return metaBaseUrl.content;
    }
    
    // Try to get from site config or detect from current path
    const path = window.location.pathname;
    const segments = path.split('/').filter(s => s);
    
    // If we're in a subdirectory like /Blogi/, use that as base
    if (segments.length > 0 && !segments[0].includes('.') && segments[0] !== 'search') {
      return '/' + segments[0];
    }
    
    return '';
  }

  // Load search index
  const baseUrl = getBaseUrl();
  const searchJsonUrl = baseUrl + '/search.json';
  
  console.log('Loading search data from:', searchJsonUrl);
  
  fetch(searchJsonUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      if (Array.isArray(data)) {
        searchIndex = data;
        console.log('Regular search index loaded:', searchIndex.length, 'items');
        
        // Check if there's a search query in the URL
        const urlParams = new URLSearchParams(window.location.search);
        const query = urlParams.get('q');
        if (query && searchInput) {
          searchInput.value = query;
          performSearch(query);
        }
      } else {
        console.error('Search data is not an array:', data);
        if (searchResults) {
          searchResults.innerHTML = '<p class="text-danger">Error loading search data. Please try again later.</p>';
        }
      }
    })
    .catch(error => {
      console.error('Error loading search index:', error);
      if (searchResults) {
        searchResults.innerHTML = '<p class="text-danger">Error loading search data. Please try again later.</p>';
      }
    });
  
  // Handle form submission
  if (searchForm) {
    searchForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const query = searchInput ? searchInput.value.trim() : '';
      if (query && query.length >= 2) {
        performSearch(query);
        // Update URL without reloading
        const newUrl = new URL(window.location);
        newUrl.searchParams.set('q', query);
        window.history.pushState({}, '', newUrl);
      } else if (searchInput) {
        searchInput.focus();
      }
    });
  }
  
  // Handle input changes for regular search (not live search)
  if (searchInput && !document.getElementById('live-search-results')) {
    searchInput.addEventListener('input', function() {
      const query = this.value.trim();
      if (query.length >= 2) {
        performSearch(query);
      } else if (searchResults) {
        searchResults.innerHTML = '<p class="search-instructions">Enter your search terms above to find content on this site.</p>';
      }
    });
  }
  
  function performSearch(query) {
    if (!searchResults) {
      return;
    }
    
    if (!searchIndex.length) {
      searchResults.innerHTML = '<p class="text-warning">Search index is still loading. Please wait a moment and try again.</p>';
      return;
    }
    
    const queryLower = query.toLowerCase();
    const queryWords = queryLower.split(' ').filter(word => word.length > 0);
    
    // Enhanced search with scoring
    const results = searchIndex.map(item => {
      let score = 0;
      const titleLower = item.title.toLowerCase();
      const contentLower = item.content ? item.content.toLowerCase() : '';
      const excerptLower = item.excerpt ? item.excerpt.toLowerCase() : '';
      
      // Title matches get highest score
      if (titleLower.includes(queryLower)) {
        score += 50;
      }
      
      // Exact title match gets even higher score
      if (titleLower === queryLower) {
        score += 100;
      }
      
      // Word matches in title
      queryWords.forEach(word => {
        if (titleLower.includes(word)) {
          score += 25;
        }
      });
      
      // Content matches
      if (contentLower.includes(queryLower)) {
        score += 20;
      }
      
      // Excerpt matches
      if (excerptLower.includes(queryLower)) {
        score += 15;
      }
      
      // Category matches
      if (item.categories && item.categories.some(category => category.toLowerCase().includes(queryLower))) {
        score += 30;
      }
      
      // Tag matches
      if (item.tags && item.tags.some(tag => tag.toLowerCase().includes(queryLower))) {
        score += 25;
      }
      
      // Word matches in content
      queryWords.forEach(word => {
        if (contentLower.includes(word)) {
          score += 5;
        }
      });
      
      return score > 0 ? { ...item, score } : null;
    }).filter(item => item !== null)
      .sort((a, b) => b.score - a.score);
    
    displayResults(results, query);
  }
  
  function displayResults(results, query) {
    if (results.length === 0) {
      searchResults.innerHTML = `
        <div class="search-no-results">
          <h3>No results found for "${query}"</h3>
          <p>Try different keywords or check your spelling.</p>
          <div class="search-suggestions">
            <p>Search suggestions:</p>
            <ul>
              <li>Use fewer keywords</li>
              <li>Check spelling</li>
              <li>Try related terms</li>
              <li>Search for specific categories or tags</li>
            </ul>
          </div>
        </div>
      `;
      return;
    }
    
    let html = `
      <div class="search-results-header">
        <h3>Found ${results.length} result${results.length !== 1 ? 's' : ''} for "${query}"</h3>
      </div>
      <div class="search-results-list">
    `;
    
    results.forEach(result => {
      const url = result.url.startsWith('/') ? result.url : '/' + result.url;
      const excerpt = result.excerpt || (result.content ? result.content.substring(0, 200) + '...' : '');
      const date = result.date || '';
      const type = result.type || 'post';
      
      // Highlight search terms in title and excerpt
      const highlightedTitle = highlightSearchTerms(result.title, query);
      const highlightedExcerpt = highlightSearchTerms(excerpt, query);
      
      html += `
        <div class="search-result-item">
          <h4><a href="${url}">${highlightedTitle}</a></h4>
          <p class="search-result-excerpt">${highlightedExcerpt}</p>
          <div class="search-result-meta">
            ${date ? `<span class="search-result-date"><i class="feather" data-feather="calendar"></i> ${date}</span>` : ''}
            ${type ? `<span class="search-result-type"><i class="feather" data-feather="file-text"></i> ${type}</span>` : ''}
            ${result.categories && result.categories.length > 0 ? `<span class="search-result-categories"><i class="feather" data-feather="folder"></i> ${result.categories.join(', ')}</span>` : ''}
            ${result.tags && result.tags.length > 0 ? `<span class="search-result-tags"><i class="feather" data-feather="tag"></i> ${result.tags.slice(0, 3).join(', ')}</span>` : ''}
          </div>
        </div>
      `;
    });
    
    html += '</div>';
    searchResults.innerHTML = html;
    
    // Initialize feather icons for the new content
    if (typeof feather !== 'undefined') {
      feather.replace();
    }
  }
  
  function highlightSearchTerms(text, query) {
    if (!text || !query) return text;
    
    const queryWords = query.toLowerCase().split(' ').filter(word => word.length > 1);
    let highlightedText = text;
    
    queryWords.forEach(word => {
      const regex = new RegExp(`(${word})`, 'gi');
      highlightedText = highlightedText.replace(regex, '<mark>$1</mark>');
    });
    
    return highlightedText;
  }
});