<script lang="ts">
  import { t } from '../../i18n.js';
  import { onMount } from 'svelte';

  export let sectionVisible: Record<string, boolean> = {};
  let sectionElement: HTMLElement;
  let progressLine: HTMLElement;
  let scrollY = 0;
  
  // We no longer need the scroll-based animation since we're using Intersection Observer
  
  // Add onMount to ensure elements are properly initialized
  onMount(() => {
    // Force a reflow to ensure the reveal elements are properly initialized
    const revealElements = sectionElement.querySelectorAll('.reveal-element');
    console.log('ProcessSection reveal elements:', revealElements.length);
    
    // Force a reflow to ensure CSS transitions work properly
    revealElements.forEach(el => {
      // This forces a reflow
      void (el as HTMLElement).offsetHeight;
    });
    
    // Set up the progress line animation
    const updateProgressLine = () => {
      if (!progressLine || !sectionElement) return;
      
      const sectionRect = sectionElement.getBoundingClientRect();
      const sectionTop = sectionRect.top;
      const sectionHeight = sectionRect.height;
      const windowHeight = window.innerHeight;
      
      // Calculate how much of the section is visible
      let progress = 0;
      
      if (sectionTop <= windowHeight * 0.2) {
        // Start filling when the section top reaches 20% from the top of viewport
        progress = Math.min(1, (windowHeight * 0.2 - sectionTop) / (sectionHeight * 0.8));
      }
      
      // Update the progress line height
      progressLine.style.height = `${progress * 100}%`;
    };
    
    // Initial update
    updateProgressLine();
    
    // Add scroll event listener
    window.addEventListener('scroll', updateProgressLine);
    
    return () => {
      window.removeEventListener('scroll', updateProgressLine);
    };
  });
</script>

<svelte:window bind:scrollY={scrollY}/>

<section 
  id="process" 
  class="process-section"
  bind:this={sectionElement}
>
  <div class="container">
    <h2 class="reveal-element">{$t.features?.landing?.process?.title || 'Our Implementation Process'}</h2>
    <p class="section-description reveal-element">{$t.features?.landing?.process?.description || 'A proven approach to seamlessly integrate AI into your business'}</p>
    
    <div class="process-steps">
      <div class="progress-line-container">
        <div class="progress-line-bg"></div>
        <div class="progress-line" bind:this={progressLine}></div>
      </div>
      
      {#each ($t.features?.landing?.process?.steps || []) as step, i}
        <div class="process-step reveal-element">
          <div class="step-content">
            <div class="step-number">{step.number}</div>
            <div class="step-text">
              <h3>{step.title}</h3>
              <p>{step.description}</p>
            </div>
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>

<style>
  .process-section {
    background-color: #000000;
    padding: 120px 0; /* Consistent padding */
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
  
  .process-steps {
    display: flex;
    flex-direction: column;
    gap: 50px;
    max-width: 800px;
    margin: 0 auto;
    position: relative;
    padding-left: 30px; /* Add space for the progress line */
  }
  
  /* Progress line styles */
  .progress-line-container {
    position: absolute;
    left: 0;
    top: 30px; /* Align with the first step number */
    bottom: 30px; /* Align with the last step number */
    width: 2px;
    z-index: 1;
  }
  
  .progress-line-bg {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.1);
  }
  
  .progress-line {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 0; /* Will be animated via JS */
    background-color: #efc824;
    transition: height 0.3s ease-out;
  }
  
  .process-step {
    position: relative;
  }
  
  .step-content {
    background-color: transparent;
    border: 1px solid #333;
    padding: 40px;
    position: relative;
    z-index: 2;
    width: 100%;
    box-sizing: border-box;
    display: flex;
    align-items: flex-start;
    gap: 30px;
    transition: background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
    text-align: left;
  }
  
  .step-content:hover {
    background-color: rgba(17, 17, 17, 0.5);
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  }
  
  .step-number {
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: 2rem;
    color: #efc824;
    background-color: transparent;
    border: 2px solid rgba(239, 200, 36, 0.3);
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  
  .step-text {
    flex: 1;
  }
  
  h3 {
    color: #efc824;
    font-size: 1.5rem;
    margin: 0 0 1.5rem;
  }
  
  p {
    color: #e3e3e3;
    margin: 0;
    line-height: 1.7;
    font-size: 1.05rem;
  }
  
  @media (max-width: 992px) {
    .process-section {
      padding: 100px 0;
    }
    
    h2 {
      font-size: 2.25rem;
    }
    
    .section-description {
      font-size: 1.125rem;
      margin-bottom: 3rem;
    }
    
    .process-steps {
      gap: 40px;
    }
  }
  
  @media (max-width: 768px) {
    .process-section {
      padding: 80px 0;
    }
    
    h2 {
      font-size: 2rem;
    }
    
    .process-steps {
      gap: 30px;
      padding-left: 20px;
    }
    
    .step-content {
      padding: 30px;
    }
    
    .step-number {
      width: 50px;
      height: 50px;
      font-size: 1.5rem;
    }
  }
</style> 