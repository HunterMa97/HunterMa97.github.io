---
layout: null
title: Haotian Ma
permalink: /
search_exclude: true
---
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Haotian Ma - Ph.D. Student @ UW-Madison</title>
  <meta name="description" content="Haotian Ma is a Ph.D. student in Computer Science at the University of Wisconsin-Madison working on explainable AI, spatial transcriptomics, and LLM interpretability." />
  <meta property="og:title" content="Haotian Ma - Homepage" />
  <meta property="og:description" content="Explainable AI in the real world, spatial transcriptomics, and LLM interpretability." />
  <meta property="og:image" content="/assets/img/haotian_profile.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Source+Serif+4:ital,opsz,wght@0,8..60,500;0,8..60,600;0,8..60,700;1,8..60,500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/landing/css/style.css?v=20260813-landing-4" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='86'>H</text></svg>" />
</head>
<body>
  <div class="progress-bar" id="progressBar"></div>

  <header class="nav" id="nav">
    <div class="nav-inner">
      <a href="#top" class="nav-brand">Haotian&nbsp;Ma</a>
      <nav class="nav-links" id="navLinks">
        <a href="#news" class="nav-link">News</a>
        <a href="#publications" class="nav-link">Publications</a>
        <a href="#experience" class="nav-link">Experience</a>
        <a href="#service" class="nav-link">Service</a>
        <a href="#life" class="nav-link">Life</a>
        <a href="#contact" class="nav-link">Contact</a>
      </nav>
      <div class="nav-actions">
        <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode">
          <svg class="icon-sun" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
          <svg class="icon-moon" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
        <button class="nav-burger" id="navBurger" aria-label="Open menu"><span></span><span></span><span></span></button>
      </div>
    </div>
  </header>

  <main id="top">
    <section class="hero">
      <div class="container hero-inner">
        <div class="hero-text">
          <p class="hero-kicker reveal">Ph.D. Student in Computer Science &middot; <a href="https://www.wisc.edu/" target="_blank" rel="noopener">University of Wisconsin-Madison</a></p>
          <h1 class="hero-name">Haotian Ma</h1>
          <p class="hero-lede reveal">I build interpretable frameworks for <span class="hl">Explainable AI in the real world</span>, from spatial transcriptomics to safer LLM deployment.</p>
          <p class="hero-bio reveal">
            I am a final year Ph.D. student in Computer Science at UW-Madison, advised by Prof. Daifeng Wang. My work applies information theory, Shapley-based attribution, and sparse autoencoder analysis to make deep learning systems more reliable and interpretable.
          </p>
          <div class="hero-cta reveal">
            <a href="#publications" class="btn btn-primary">View Publications</a>
            <a href="mailto:hma232@wisc.edu" class="btn btn-outline">Email Me</a>
          </div>
          <div class="hero-socials reveal" id="heroSocials"></div>
        </div>
        <figure class="hero-photo photo-frame reveal">
          <img src="/assets/img/haotian_profile.png" alt="Portrait of Haotian Ma" loading="eager" />
          <figcaption>Explainable AI &middot; Spatial Transcriptomics &middot; LLM Interpretability</figcaption>
        </figure>
      </div>
      <a href="#news" class="scroll-hint" aria-label="Scroll down"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg></a>
    </section>

    <section class="section section-alt" id="news">
      <div class="container">
        <h2 class="section-title reveal">News</h2>
        <ul class="news-list" id="newsList"></ul>
        <button class="btn btn-ghost" id="newsToggle" hidden>Show older news</button>
      </div>
    </section>

    <section class="section" id="publications">
      <div class="container">
        <h2 class="section-title reveal">Publications</h2>
        <p class="section-note reveal">Selected shows the focused set by default. Switch to All for the complete list.</p>
        <div class="pub-filters reveal" id="pubFilters">
          <button class="filter-btn active" data-filter="selected">Selected</button>
          <button class="filter-btn" data-filter="all">All</button>
          <input type="search" id="pubSearch" class="pub-search" placeholder="Search title, venue, author..." aria-label="Search publications" />
        </div>
        <div class="pub-list" id="pubList"></div>
        <p class="pub-empty" id="pubEmpty" hidden>No publications match your filter or search.</p>
      </div>
    </section>

    <section class="section section-alt" id="experience">
      <div class="container">
        <h2 class="section-title reveal">Experience &amp; Education</h2>
        <div class="timeline" id="timeline"></div>
      </div>
    </section>

    <section class="section" id="service">
      <div class="container two-col">
        <div>
          <h2 class="section-title reveal">Service</h2>
          <ul class="simple-list" id="serviceList"></ul>
        </div>
        <div>
          <h2 class="section-title reveal">Open To</h2>
          <ul class="simple-list" id="openToList"></ul>
        </div>
      </div>
    </section>

    <section class="section section-alt" id="life">
      <div class="container">
        <div class="after-hours reveal">
          <div class="after-hours-copy">
            <p class="after-hours-kicker">Life</p>
            <h2>Stories, systems, and imagined worlds</h2>
            <p>Outside of research, I enjoy writing, game design, and watching TV series. In 2025, I finished the first book of my life: a 300,000-word novel with dozens of characters and an intricate plot, about political intrigue, human nature, and war. After I graduate, I will look for ways to share it, perhaps through self-publishing, a visual novel, or AI-generated video.</p>
          </div>
          <div class="after-hours-card">
            <span class="mono">after hours</span>
            <strong>writing &middot; game design &middot; TV series</strong>
            <p>It's alsk about real people in the real world.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section contact-section" id="contact">
      <div class="container contact-wrap reveal">
        <h2 class="section-title centered">Get in Touch</h2>
        <p class="contact-text">I enjoy talking with people and working together. If you have an idea to share, are looking for potential ways to collaborate, or would like to invite me to review, feel free to reach out.</p>
        <div class="contact-email">
          <a href="mailto:hma232@wisc.edu" class="btn btn-primary btn-large">hma232@wisc.edu</a>
          <button class="btn btn-outline btn-large copy-email" id="copyEmail" data-email="hma232@wisc.edu">Copy</button>
        </div>
        <div class="hero-socials contact-socials" id="contactSocials"></div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container"><p>&copy; 2026 Haotian Ma &middot; Built with Jekyll and al-folio</p></div>
  </footer>

  <button class="back-to-top" id="backToTop" aria-label="Back to top"><svg class="btt-ring" viewBox="0 0 46 46" aria-hidden="true"><circle cx="23" cy="23" r="20"/></svg><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 15l-6-6-6 6"/></svg></button>
  <div class="toast" id="toast">Copied to clipboard</div>

  <script src="/assets/landing/js/data.js?v=20260813-landing-4"></script>
  <script src="/assets/landing/js/main.js?v=20260813-landing-4"></script>
</body>
</html>
