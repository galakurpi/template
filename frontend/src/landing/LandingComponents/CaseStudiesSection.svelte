<script lang="ts">
  import { t } from '../../i18n.js';
  import { onMount } from 'svelte';

  export let sectionVisible: Record<string, boolean> = {};
  let sectionElement: HTMLElement;
  
  // We no longer need the scroll-based animation since we're using Intersection Observer
  
  // Add onMount to ensure elements are properly initialized
  onMount(() => {
    if (sectionElement) {
      const revealElements = sectionElement.querySelectorAll('.reveal-element');
      console.log('CaseStudiesSection reveal elements:', revealElements.length);
      
      revealElements.forEach(el => {
        void (el as HTMLElement).offsetHeight;
      });
    }
  });
</script>

<section id="case-studies" class="case-studies-section" bind:this={sectionElement}>
  <div class="container">
    <h2 class="reveal-element">{$t.features?.landing?.caseStudies?.title || 'Solutions'}</h2>
    <p class="section-description reveal-element">{$t.features?.landing?.caseStudies?.description || 'Here are some examples of our solutions:'}</p>
    
    <div class="cases-list">
      {#each ($t.features?.landing?.caseStudies?.cases || []) as case_study}
        <div class="case-card reveal-element">
          <div class="case-content">
            <span class="industry">{case_study.industry}</span>
            <h3>{case_study.title}</h3>
            <p class="description">{case_study.description}</p>
            <ul class="metrics">
              {#each case_study.metrics as metric}
                <li>{metric}</li>
              {/each}
            </ul>
          </div>
        </div>
      {/each}

      <!-- Endless Possibilities Section -->
      <div class="case-card possibilities-card reveal-element">
        <div class="case-content">
          <h3>{$t.features?.landing?.caseStudies?.possibilities?.title || 'Endless Possibilities'}</h3>
          <p class="possibilities-text">
            {$t.features?.landing?.caseStudies?.possibilities?.conclusion || 'We have identified and designed specific automations internally that we are now ready to implement in our and other businesses.'}
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  .case-studies-section {
    background-color: #000000;
    padding: 120px 0;
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
  
  .cases-list {
    display: flex;
    flex-direction: column;
    gap: 50px;
    max-width: 800px;
    margin: 0 auto;
  }
  
  .case-card {
    position: relative;
    background-color: transparent;
    border: 1px solid #333;
    padding: 40px;
  }
  
  .case-content {
    background-color: transparent;
    color: #e3e3e3;
    text-align: left;
    width: 100%;
    box-sizing: border-box;
    transition: background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .case-card:hover .case-content {
    background-color: rgba(17, 17, 17, 0.5);
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  }
  
  .industry {
    color: #efc824;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 1rem;
    display: block;
  }
  
  h3 {
    color: #efc824;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .metrics {
    list-style: none;
    padding: 0;
    margin: 2rem 0 0;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
  }
  
  .metrics li {
    position: relative;
    margin: 0;
    padding: 1rem;
    font-size: 1rem;
    color: #e3e3e3;
    background-color: rgba(239, 200, 36, 0.05); 
    border-left: 3px solid #efc824;
    transition: transform 0.3s ease, background-color 0.3s ease;
  }

  .metrics li:hover {
    transform: translateX(5px);
    background-color: rgba(239, 200, 36, 0.1);
  }

  .description {
    font-size: 1.1rem;
    line-height: 1.7;
    margin-bottom: 1rem;
    white-space: pre-line;
    color: #e3e3e3;
    opacity: 0.9;
  }

  /* Possibilities Card Specific Styles */
  .possibilities-card {
    margin-top: 2rem;
  }

  .possibilities-text {
    color: #e3e3e3;
    font-size: 1.1rem;
    line-height: 1.7;
    margin-top: 1rem;
  }

  @media (max-width: 768px) {
    .case-studies-section {
      padding: 80px 0;
    }
    
    h2 {
      font-size: 2rem;
    }
    
    .section-description {
      font-size: 1.125rem;
      margin-bottom: 3rem;
    }
    
    .case-card {
      padding: 30px;
    }
    
    .metrics {
      grid-template-columns: 1fr;
      gap: 1rem;
    }
    
    .metrics li {
      padding: 0.875rem;
      font-size: 0.95rem;
    }
  }

  @media (max-width: 480px) {
    .case-studies-section {
      padding: 60px 0;
    }
    
    h2 {
      font-size: 1.75rem;
    }
    
    .section-description {
      font-size: 1rem;
      margin-bottom: 2rem;
    }
    
    .case-card {
      padding: 20px;
    }
    
    .metrics li {
      padding: 0.75rem;
      font-size: 0.9rem;
    }
  }
</style> 