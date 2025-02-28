<script lang="ts">
  import { t } from '../../i18n.js';
  import { onMount } from 'svelte';

  export let sectionVisible: Record<string, boolean> = {};
  let scrollY: number = 0;
  
  // Function to initialize the animated geometric background
  let canvas: HTMLCanvasElement;
  let ctx: CanvasRenderingContext2D | null;
  
  interface Node {
    x: number;
    y: number;
    vx: number;
    vy: number;
  }
  
  interface Line {
    start: Node;
    end: Node;
    opacity: number;
    pulseDirection: number;
    pulseSpeed: number;
  }
  
  let sectionElement: HTMLElement;
  
  onMount(() => {
    if (typeof window !== 'undefined') {
      initGeometricBackground();
      window.addEventListener('resize', initGeometricBackground);
      
      return () => {
        window.removeEventListener('resize', initGeometricBackground);
        if (ctx && ctx.canvas) {
          ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        }
      };
    }
    
    // Force a reflow to ensure the reveal elements are properly initialized
    const revealElements = sectionElement.querySelectorAll('.reveal-element');
    console.log('HeroSection reveal elements:', revealElements.length);
    
    // Force a reflow to ensure CSS transitions work properly
    revealElements.forEach(el => {
      // This forces a reflow
      void (el as HTMLElement).offsetHeight;
    });
  });
  
  function initGeometricBackground() {
    if (!canvas) return;
    
    const dpr = window.devicePixelRatio || 1;
    canvas.width = window.innerWidth * dpr;
    canvas.height = window.innerHeight * dpr;
    
    ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    ctx.scale(dpr, dpr);
    
    // Set canvas dimensions in CSS
    canvas.style.width = window.innerWidth + 'px';
    canvas.style.height = window.innerHeight + 'px';
    
    // Clear previous drawings
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Create geometric shapes
    const lines: Line[] = [];
    const nodeCount = Math.floor(window.innerWidth / 200) + 8; // Fewer nodes, more stable
    
    // Create nodes (points)
    const nodes: Node[] = [];
    for (let i = 0; i < nodeCount; i++) {
      nodes.push({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        vx: (Math.random() - 0.5) * 0.15, // Slower movement
        vy: (Math.random() - 0.5) * 0.15
      });
    }
    
    // Create connections between more nodes
    for (let i = 0; i < nodes.length; i++) {
      const connectionsCount = Math.floor(Math.random() * 2) + 2; // 2-3 connections per node
      
      for (let j = 0; j < connectionsCount; j++) {
        const targetIndex = Math.floor(Math.random() * nodes.length);
        if (targetIndex !== i) {
          lines.push({
            start: nodes[i],
            end: nodes[targetIndex],
            opacity: Math.random() * 0.4 + 0.3, // More consistent opacity
            pulseDirection: Math.random() > 0.5 ? 1 : -1,
            pulseSpeed: Math.random() * 0.005 + 0.001 // Slower pulse for less appearing/disappearing
          });
        }
      }
    }
    
    // Add some random standalone lines for visual interest
    for (let i = 0; i < nodeCount / 4; i++) {
      const x1 = Math.random() * window.innerWidth;
      const y1 = Math.random() * window.innerHeight;
      const length = Math.random() * 80 + 30; // Smaller line length
      const angle = Math.random() * Math.PI * 2;
      
      const startNode: Node = {
        x: x1,
        y: y1,
        vx: (Math.random() - 0.5) * 0.05, // Much slower movement
        vy: (Math.random() - 0.5) * 0.05
      };
      
      const endNode: Node = {
        x: x1 + Math.cos(angle) * length,
        y: y1 + Math.sin(angle) * length,
        vx: (Math.random() - 0.5) * 0.05,
        vy: (Math.random() - 0.5) * 0.05
      };
      
      lines.push({
        start: startNode,
        end: endNode,
        opacity: Math.random() * 0.4 + 0.3,
        pulseDirection: Math.random() > 0.5 ? 1 : -1,
        pulseSpeed: Math.random() * 0.005 + 0.001
      });
      
      nodes.push(startNode, endNode);
    }
    
    // Draw and animate
    function draw() {
      if (!ctx) return;
      
      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Draw lines
      lines.forEach(line => {
        if (!ctx) return;
        
        // Update opacity for pulsing effect
        line.opacity += line.pulseSpeed * line.pulseDirection;
        if (line.opacity > 0.7) {
          line.opacity = 0.7;
          line.pulseDirection = -1;
        } else if (line.opacity < 0.2) { // Higher minimum opacity for less disappearing
          line.opacity = 0.2;
          line.pulseDirection = 1;
        }
        
        ctx.beginPath();
        ctx.strokeStyle = `rgba(239, 200, 36, ${line.opacity})`;
        ctx.lineWidth = 0.5; // Thinner lines
        ctx.moveTo(line.start.x, line.start.y);
        ctx.lineTo(line.end.x, line.end.y);
        ctx.stroke();
      });
      
      // Move nodes
      nodes.forEach(node => {
        node.x += node.vx;
        node.y += node.vy;
        
        // Bounce off edges with less speed change
        if (node.x < 0 || node.x > window.innerWidth) {
          node.vx *= -0.95; // Slightly reduce speed on bounce
          node.x = node.x < 0 ? 0 : window.innerWidth;
        }
        if (node.y < 0 || node.y > window.innerHeight) {
          node.vy *= -0.95;
          node.y = node.y < 0 ? 0 : window.innerHeight;
        }
      });
      
      requestAnimationFrame(draw);
    }
    
    draw();
  }
</script>

<svelte:window bind:scrollY={scrollY}/>

<section id="hero" class="hero-section" class:visible={sectionVisible['hero'] || false} bind:this={sectionElement}>
  <canvas bind:this={canvas} class="geometric-bg"></canvas>
  <div class="container">
    <div class="hero-content">
      <h1 class="reveal-element" style="transform: translateY({scrollY * 0.2}px);">{$t.features.hero?.title || 'AI Automation for Real Business Results'}</h1>
      <p class="subtitle reveal-element" style="transform: translateY({scrollY * 0.2}px);">{$t.features?.landing?.hero?.subtitle || 'Practical AI solutions that save time, reduce costs, and drive growth'}</p>
      <div class="cta-buttons reveal-element" style="transform: translateY({scrollY * 0.2}px);">
        <a href="/landing/contact/" class="btn btn-primary">
          {$t.features?.landing?.hero?.primaryButton || 'Contact Us'}
        </a>
      </div>
    </div>
  </div>
</section>

<style>
  .hero-section {
    background-color: #000000;
    min-height: 100vh; /* Take full viewport height */
    display: flex;
    align-items: center;
    position: relative;
    overflow: hidden;
    padding: 0; /* Remove padding since we're using min-height: 100vh */
  }
  
  /* Geometric background canvas */
  .geometric-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
  }
  
  .hero-content {
    max-width: 800px;
    position: relative;
    z-index: 2;
  }
  
  h1 {
    margin: 0;
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: 4rem;
    line-height: 1.2;
    margin-bottom: 2rem;
    color: #efc824;
    will-change: transform;
    transition: transform 0.1s ease-out;
  }
  
  .subtitle {
    font-size: 1.5rem;
    color: #e3e3e3;
    margin-bottom: 3rem;
    max-width: 700px;
    will-change: transform;
    transition: transform 0.1s ease-out;
  }
  
  .cta-buttons {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    will-change: transform;
    transition: transform 0.1s ease-out;
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
    margin-bottom: 12px;
  }
  
  .btn-primary {
    background-color: #efc824;
    color: #000000;
  }
  
  .btn-primary:hover {
    background-color: #f5d547;
  }
  
  @media (max-width: 992px) {
    h1 {
      font-size: 3rem;
    }
    
    .subtitle {
      font-size: 1.25rem;
    }
  }
  
  @media (max-width: 768px) {
    h1 {
      font-size: 2.5rem;
    }
    
    .subtitle {
      font-size: 1.125rem;
    }
  }
  
  .hero-subtitle {
    color: #e3e3e3;
    font-size: 1.25rem;
    max-width: 800px;
    margin: 2rem auto 3rem;
    text-align: center;
    white-space: pre-line; /* Added to preserve line breaks */
  }
</style> 