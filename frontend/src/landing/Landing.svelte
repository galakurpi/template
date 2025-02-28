<script lang="ts">
  import PublicNavbar from '../common/PublicNavbar.svelte';
  import Footer from '../common/footer.svelte';
  import { onMount } from 'svelte';
  import { t } from '../i18n.js';
  
  // Import modular components
  import HeroSection from './LandingComponents/HeroSection.svelte';
  import BenefitsSection from './LandingComponents/BenefitsSection.svelte';
  import ProcessSection from './LandingComponents/ProcessSection.svelte';
  import CaseStudiesSection from './LandingComponents/CaseStudiesSection.svelte';
  import CtaSection from './LandingComponents/CtaSection.svelte';
  
  let sectionVisible: Record<string, boolean> = {};
  let scrollY: number;
  let debugMode = false;
  
  onMount(() => {
    // Add a small delay to ensure all components are fully rendered
    setTimeout(() => {
      // First, make sure all reveal elements have the initial state properly set
      const allRevealElements = document.querySelectorAll('.reveal-element');
      console.log('Total reveal elements found:', allRevealElements.length);
      
      // Force a reflow on all elements to ensure CSS transitions work properly
      allRevealElements.forEach(el => {
        // Reset any existing visible class that might have been applied
        el.classList.remove('visible');
        // Force a reflow
        void (el as HTMLElement).offsetHeight;
      });
      
      // Now set up the intersection observer
      const elementObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            // Add visible class to the element
            entry.target.classList.add('visible');
            console.log('Element visible:', entry.target);
          }
        });
      }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
      
      // Observe all elements with the 'reveal-element' class
      allRevealElements.forEach(element => {
        elementObserver.observe(element);
        
        // Check if element is already in viewport and make it visible immediately
        const rect = element.getBoundingClientRect();
        if (rect.top < window.innerHeight) {
          element.classList.add('visible');
        }
      });
      
      // Section visibility for component-level animations (keep for backward compatibility)
      const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            sectionVisible[entry.target.id] = true;
          }
        });
      }, { threshold: 0.1 });
      
      document.querySelectorAll('section').forEach(section => {
        sectionObserver.observe(section);
      });
    }, 300); // Increased delay to ensure DOM is ready
    
    // Set up parallax effect ONLY for the hero section
    const heroParallaxElements = document.querySelectorAll('.hero-parallax');
    
    const handleScroll = () => {
      heroParallaxElements.forEach((element: Element) => {
        const speedMultiplier = parseFloat((element as HTMLElement).dataset.speed || '0.5');
        // Limit the maximum offset to prevent elements from overlapping too much
        const maxOffset = 80; // Reduced from 100 to ensure less overlap
        const offset = Math.min(maxOffset, window.scrollY * speedMultiplier);
        
        // Apply transform based on element's data-direction (up/down)
        if ((element as HTMLElement).dataset.direction === 'up') {
          (element as HTMLElement).style.transform = `translateY(-${offset}px)`;
        } else {
          (element as HTMLElement).style.transform = `translateY(${offset}px)`;
        }
      });
    };
    
    window.addEventListener('scroll', handleScroll);
    
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  });


  // Form values
  let name = '';
  let email = '';
  let role = '';
  let companyName = '';
  let companyWebsite = '';
  let companySize = 'Less than 20 people';
  let annualRevenue = 'Less than $100K/month';
  let projectBudget = '$0 - $5000';
  let services = 'Developing a custom AI solution';
  let helpText = '';


</script>

<svelte:window bind:scrollY={scrollY}/>

<svelte:head>
  <title>{$t.features?.landing?.meta?.title || 'AI Automation Solutions for Businesses | Yekar'}</title>
  <meta name="description" content={$t.features?.landing?.meta?.description || 'Transform your business operations with our AI automation solutions. Increase efficiency, reduce costs, and improve customer experience with Yekar.'}>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@900&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
</svelte:head>

<div class="landing-page" class:debug-mode={debugMode}>
  <PublicNavbar currentPage="landing" />
  
  <div class="content-wrapper">
    <!-- Hero section with parallax -->
    <div class="parallax-wrapper">
      <div class="hero-parallax" data-speed="0.05" data-direction="up">
        <HeroSection {sectionVisible} />
      </div>
    </div>
    
    <!-- Regular sections without parallax -->
    <div class="regular-section">
      <BenefitsSection {sectionVisible} />
    </div>
    
    <div class="regular-section">
      <ProcessSection {sectionVisible} />
    </div>
    
    <div class="regular-section">
      <CaseStudiesSection {sectionVisible} />
    </div>
    
    <div class="regular-section">
      <CtaSection {sectionVisible} />
    </div>
  </div>
  
  <Footer />
</div>

<style>
  /* General Styles */
  .landing-page {
    color: #e3e3e3;
    font-family: 'Roboto', sans-serif;
    background-color: #000000;
    position: relative;
    overflow: hidden;
  }
  
  .content-wrapper {
    position: relative;
    overflow: hidden;
  }
  
  .parallax-wrapper {
    position: relative;
    overflow: hidden;
    margin-bottom: 60px;
  }
  
  .hero-parallax {
    position: relative;
    will-change: transform;
    z-index: 1;
  }
  
  .regular-section {
    position: relative;
    margin-bottom: 60px;
    z-index: 1;
  }
  
  :global(.landing-page .container) {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 40px;
  }
  
  /* Section level animations - keeping for backward compatibility */
  :global(.landing-page section) {
    padding: 120px 0; /* Consistent vertical padding */
    background-color: #000000; /* Ensure all sections have black background */
    position: relative;
    z-index: 1; /* Ensure proper stacking */
  }
  
  /* Element level animations - new approach */
  :global(.reveal-element) {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s cubic-bezier(0.25, 0.1, 0.25, 1), 
                transform 0.8s cubic-bezier(0.25, 0.1, 0.25, 1);
    will-change: opacity, transform;
    /* Add a small delay to ensure transitions work properly */
    transition-delay: 0.1s;
  }
  
  :global(.reveal-element.visible) {
    opacity: 1 !important;
    transform: translateY(0) !important;
  }
  
  /* Staggered reveal for elements within the same container */
  :global(.benefits-list .reveal-element:nth-child(1)) { transition-delay: 0.1s; }
  :global(.benefits-list .reveal-element:nth-child(2)) { transition-delay: 0.2s; }
  :global(.benefits-list .reveal-element:nth-child(3)) { transition-delay: 0.3s; }
  :global(.benefits-list .reveal-element:nth-child(4)) { transition-delay: 0.4s; }
  
  :global(.process-steps .reveal-element:nth-child(1)) { transition-delay: 0.1s; }
  :global(.process-steps .reveal-element:nth-child(2)) { transition-delay: 0.2s; }
  :global(.process-steps .reveal-element:nth-child(3)) { transition-delay: 0.3s; }
  :global(.process-steps .reveal-element:nth-child(4)) { transition-delay: 0.4s; }
  
  :global(.cases-list .reveal-element:nth-child(1)) { transition-delay: 0.1s; }
  :global(.cases-list .reveal-element:nth-child(2)) { transition-delay: 0.2s; }
  :global(.cases-list .reveal-element:nth-child(3)) { transition-delay: 0.3s; }
  
  /* Add consistent delays for section titles and descriptions */
  :global(section h2.reveal-element) { transition-delay: 0.1s; }
  :global(section .section-description.reveal-element) { transition-delay: 0.2s; }
  
  /* Make all elements visible initially for debugging */
  :global(.debug-mode .reveal-element) {
    opacity: 1 !important;
    transform: translateY(0) !important;
  }
  
  /* Keep section visibility for backward compatibility */
  :global(.landing-page section.visible) {
    opacity: 1;
    transform: translateY(0);
  }
  
  /* Responsive adjustments */
  @media (max-width: 992px) {
    .regular-section {
      margin-bottom: 40px;
    }
    
    :global(.landing-page section) {
      padding: 100px 0; /* Adjusted padding for medium screens */
    }
  }
  
  @media (max-width: 768px) {
    :global(.landing-page .container) {
      padding: 0 24px;
    }
    
    .regular-section {
      margin-bottom: 30px;
    }
    
    :global(.landing-page section) {
      padding: 80px 0; /* Adjusted padding for small screens */
    }
  }
  
</style> 