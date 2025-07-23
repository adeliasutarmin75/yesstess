---
layout: page
title: Cookie Policy
permalink: /cookie-policy/
---

# Cookie Policy

**Effective Date: {{ site.time | date: "%B %d, %Y" }}**

## What Are Cookies

Cookies are small text files that are placed on your computer or mobile device when you visit our website {{ site.url }}{{ site.baseurl }}. They are widely used to make websites work more efficiently and provide information to website owners.

## How We Use Cookies

We use cookies for the following purposes:

### Essential Cookies
- **Site functionality**: These cookies are necessary for the website to function properly
- **Security**: Help us identify and prevent security risks
- **Preferences**: Remember your settings and preferences

### Analytics Cookies
- **Usage analytics**: Help us understand how visitors interact with our website
- **Performance monitoring**: Allow us to improve website performance
- **Content optimization**: Help us determine which content is most valuable to users

### Advertising Cookies (if applicable)
{% if site.adsense.client_id and site.adsense.client_id != "" %}
- **Personalized ads**: Deliver relevant advertisements based on your interests
- **Ad performance**: Measure the effectiveness of advertising campaigns
- **Frequency capping**: Limit the number of times you see the same ad
{% else %}
We do not currently use advertising cookies on this website.
{% endif %}

## Types of Cookies We Use

### First-Party Cookies
Cookies set directly by our website to improve your browsing experience.

### Third-Party Cookies
Cookies set by external services we use, such as:

{% if site.google_analytics and site.google_analytics != "" %}
- **Google Analytics**: For website analytics and performance monitoring
{% endif %}
{% if site.disqus.shortname and site.disqus.shortname != "" %}
- **Disqus**: For comment functionality
{% endif %}
{% if site.adsense.client_id and site.adsense.client_id != "" %}
- **Google AdSense**: For displaying advertisements
{% endif %}

## Managing Your Cookie Preferences

You can control and manage cookies in several ways:

### Browser Settings
Most web browsers allow you to:
- View what cookies you have and delete them individually
- Block third-party cookies
- Block cookies from particular sites
- Block all cookies from being set
- Delete all cookies when you close your browser

### Opt-Out Tools
You can opt out of certain cookies through these tools:
- [Google Analytics Opt-out](https://tools.google.com/dlpage/gaoptout)
- [Google Ads Settings](https://adssettings.google.com/)
- [Network Advertising Initiative](http://www.networkadvertising.org/choices/)

## Impact of Disabling Cookies

If you choose to disable cookies, some features of our website may not function properly, including:
- Remembering your preferences
- Staying logged in (if applicable)
- Providing personalized content
- Analytics and performance monitoring

## Cookie Retention

Different cookies have different retention periods:
- **Session cookies**: Deleted when you close your browser
- **Persistent cookies**: Remain for a set period or until manually deleted
- **Analytics cookies**: Typically retained for 24-26 months

## Updates to This Policy

We may update this Cookie Policy from time to time to reflect changes in our practices or for other operational, legal, or regulatory reasons.

## Contact Us

If you have any questions about our use of cookies, please contact us at:

**Email:** {{ site.email }}  
**Website:** {{ site.url }}{{ site.baseurl }}

## More Information

For more information about cookies and how they work, visit:
- [All About Cookies](https://www.allaboutcookies.org/)
- [Your Online Choices](https://www.youronlinechoices.com/)

---

*Last updated: {{ site.time | date: "%B %d, %Y" }}*