// Cloudflare Workers Site Optimization

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  // Performance optimizations for Cloudflare
  const response = await fetch(request)
  const modifiedResponse = new Response(response.body, response)
  
  // Add performance headers
  modifiedResponse.headers.set('X-Content-Type-Options', 'nosniff')
  modifiedResponse.headers.set('X-Frame-Options', 'DENY')
  modifiedResponse.headers.set('X-XSS-Protection', '1; mode=block')
  modifiedResponse.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  
  // Cache control for static assets
  const url = new URL(request.url)
  
  if (url.pathname.startsWith('/assets/')) {
    modifiedResponse.headers.set('Cache-Control', 'public, max-age=31536000, immutable')
  }
  
  if (url.pathname.endsWith('.html') || url.pathname === '/') {
    modifiedResponse.headers.set('Cache-Control', 'public, max-age=300, s-maxage=86400')
  }
  
  // Add preload headers for critical resources
  if (url.pathname === '/') {
    modifiedResponse.headers.set('Link', '</assets/css/main.css>; rel=preload; as=style, </assets/js/main.js>; rel=preload; as=script')
  }
  
  return modifiedResponse
}