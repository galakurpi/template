<script lang="ts">
  import { t } from '../../i18n.js';
  import { onMount } from 'svelte';

  export let sectionVisible: Record<string, boolean> = {};
  let sectionElement: HTMLElement;
  
  // We no longer need the scroll-based animation since we're using Intersection Observer
  
  // Add onMount to ensure elements are properly initialized
  onMount(() => {
    // Make sure sectionElement is defined before trying to use it
    if (sectionElement) {
      // Force a reflow to ensure the reveal elements are properly initialized
      const revealElements = sectionElement.querySelectorAll('.reveal-element');
      console.log('CtaSection reveal elements:', revealElements.length);
      
      // Force a reflow to ensure CSS transitions work properly
      revealElements.forEach(el => {
        // This forces a reflow
        void (el as HTMLElement).offsetHeight;
      });
    }
  });
</script>

<section id="cta" class="cta-section" class:visible={sectionVisible['cta'] || false} bind:this={sectionElement}>
  <div class="container">
    <h2 class="reveal-element">{$t.features?.landing?.cta?.title || 'Ready to Transform Your Business?'}</h2>
    <p class="cta-description reveal-element">{$t.features?.landing?.cta?.description || 'Schedule a free consultation to discuss how AI automation can address your specific business challenges'}</p>
    <div class="cta-buttons reveal-element">
      <a href="/landing/contact/" class="btn btn-primary">
        {$t.features?.landing?.cta?.primaryButton || 'Contact Us'}
      </a>
    </div>
  </div>
</section>

<style>
  .cta-section {
    background-color: #000000;
    padding: 120px 0;
    margin-bottom: 120px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }
  
  .cta-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E%3Cg fill='%23efc824' fill-opacity='0.05'%3E%3Cpath d='M0 0h40v40H0V0zm40 40h40v40H40V40zm0-40h2l-2 2V0zm0 4l4-4h2l-6 6V4zm0 4l8-8h2L40 10V8zm0 4L52 0h2L40 14v-2zm0 4L56 0h2L40 18v-2zm0 4L60 0h2L40 22v-2zm0 4L64 0h2L40 26v-2zm0 4L68 0h2L40 30v-2zm0 4L72 0h2L40 34v-2zm0 4L76 0h2L40 38v-2zm0 4L80 0v2L42 40h-2zm4 0L80 4v2L46 40h-2zm4 0L80 8v2L50 40h-2zm4 0l28-28v2L54 40h-2zm4 0l24-24v2L58 40h-2zm4 0l20-20v2L62 40h-2zm4 0l16-16v2L66 40h-2zm4 0l12-12v2L70 40h-2zm4 0l8-8v2l-6 6h-2zm4 0l4-4v2l-2 2h-2z'/%3E%3C/g%3E%3C/svg%3E");
    z-index: 0;
    opacity: 0.1;
  }
  
  .container {
    position: relative;
    z-index: 1;
  }
  
  h2 {
    color: #efc824;
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: 3rem;
    margin-bottom: 2rem;
  }
  
  .cta-description {
    color: #e3e3e3;
    font-size: 1.25rem;
    max-width: 800px;
    margin: 0 auto 4rem;
    text-align: center;
    white-space: pre-line;
  }
  
  .cta-buttons {
    display: flex;
    justify-content: center;
    gap: 16px;
    flex-wrap: wrap;
  }
  
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 16px 32px;
    border-radius: 0;
    font-weight: 600;
    transition: all 0.3s ease;
    text-decoration: none;
    gap: 12px;
  }
  
  .btn-primary {
    background-color: #efc824;
    color: #1b1b1b;
  }
  
  .btn-primary:hover {
    background-color: #f5d547;
  }
  
  @media (max-width: 992px) {
    .cta-section {
      padding: 100px 0;
    }
    
    h2 {
      font-size: 2.5rem;
    }
    
    .cta-description {
      font-size: 1.125rem;
    }
  }
  
  @media (max-width: 768px) {
    .cta-section {
      padding: 80px 0;
    }
    
    h2 {
      font-size: 2rem;
    }
  }
</style> 