<script lang="ts">
  import { t } from '../../i18n.js';
  import { onMount } from 'svelte';

  export let sectionVisible: Record<string, boolean> = {};
  let sectionElement: HTMLElement;
  
  // We no longer need the scroll-based animation since we're using Intersection Observer

  // Add onMount to ensure elements are properly initialized
  onMount(() => {
    // Force a reflow to ensure the reveal elements are properly initialized
    const revealElements = sectionElement.querySelectorAll('.reveal-element');
    console.log('BenefitsSection reveal elements:', revealElements.length);
    
    // Force a reflow to ensure CSS transitions work properly
    revealElements.forEach(el => {
      // This forces a reflow
      void (el as HTMLElement).offsetHeight;
    });
  });
</script>

<section id="benefits" class="benefits-section" bind:this={sectionElement}>
  <div class="container">
    <h2 class="reveal-element">{$t.features?.landing?.benefits?.title || 'Why Choose AI Automation?'}</h2>
    <p class="section-description reveal-element">{$t.features?.landing?.benefits?.description || 'Our AI solutions provide tangible benefits that impact your bottom line'}</p>
    
    <div class="benefits-list">
      {#each ($t.features?.landing?.benefits?.items || []) as benefit, i}
        <div class="benefit-card reveal-element">
          <div class="benefit-content">
            <h3>{benefit.title}</h3>
            <p>{benefit.description}</p>
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>

<style>
  .benefits-section {
    background-color: #000000;
    padding: 120px 0; /* Consistent padding */
    text-align: center;
    position: relative;
    z-index: 1;
  }
  
  h2 {
    color: #efc824;
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
  }
  
  .section-description {
    color: #e3e3e3;
    font-size: 1.25rem;
    max-width: 800px;
    margin: 0 auto 4rem;
    text-align: center;
    white-space: pre-line;
  }
  
  .benefits-list {
    display: flex;
    flex-direction: column;
    gap: 50px; /* Consistent gap with other sections */
    max-width: 800px;
    margin: 0 auto;
  }
  
  .benefit-card {
    position: relative;
  }
  
  .benefit-content {
    background-color: transparent;
    border: 1px solid #333;
    padding: 40px;
    text-align: left;
    width: 100%;
    box-sizing: border-box;
    transition: background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .benefit-content:hover {
    background-color: rgba(17, 17, 17, 0.5);
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  }
  
  h3 {
    color: #efc824;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  p {
    color: #e3e3e3;
    line-height: 1.7;
    font-size: 1.05rem;
    margin: 0;
    white-space: pre-line;
  }
  
  @media (max-width: 992px) {
    .benefits-section {
      padding: 100px 0;
    }
    
    h2 {
      font-size: 2.25rem;
    }
    
    .section-description {
      font-size: 1.125rem;
      margin-bottom: 3rem;
    }
    
    .benefits-list {
      gap: 40px;
    }
  }
  
  @media (max-width: 768px) {
    .benefits-section {
      padding: 80px 0;
    }
    
    h2 {
      font-size: 2rem;
    }
    
    .benefit-content {
      padding: 30px;
    }
    
    .benefits-list {
      gap: 30px;
    }
  }
</style> 