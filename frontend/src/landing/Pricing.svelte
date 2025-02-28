<script lang="ts">
    //@ts-nocheck
    import PublicNavbar from '../common/PublicNavbar.svelte';
    import Footer from '../common/footer.svelte';
    import { ChevronRight, Check } from 'lucide-svelte';
    import Testimonials from './Testimonials.svelte';
    import FAQ from './FAQ.svelte';
    import { onMount } from 'svelte';
    import { t } from '../i18n.js';

    let fromStartNow = false;
    let mounted = false;
    const whatsappLink = "https://wa.me/34747405452";

    // Function to set cookie
    function setCookie(name: string, value: string, days: number = 30) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = `expires=${date.toUTCString()}`;
        document.cookie = `${name}=${value};${expires};path=/`;
    }

    onMount(() => {
        mounted = true;
        const urlParams = new URLSearchParams(window.location.search);
        fromStartNow = urlParams.get('from') === 'start_now';

        // Check URL for affiliate code
        const affiliateCode = urlParams.get('ref');
        
        // If affiliate code is found in URL, save it to cookie
        if (affiliateCode) {
            setCookie('affiliate_code', affiliateCode);
            console.log('Affiliate code from URL stored in cookie:', affiliateCode);
        }
    });

    function handleStartNowClick(event: MouseEvent) {
        event.preventDefault();
        window.location.href = "/register";
    }

    function handleContactUsClick(event: MouseEvent) {
        event.preventDefault();
        window.location.href = whatsappLink;
    }

    $: testimonials = [
        { 
            name: $t.testimonials?.items?.[0]?.name , 
            role: $t.testimonials?.items?.[0]?.role , 
            quote: $t.testimonials?.items?.[0]?.quote  
        },
        { 
            name: $t.testimonials?.items?.[1]?.name , 
            role: $t.testimonials?.items?.[1]?.role , 
            quote: $t.testimonials?.items?.[1]?.quote  
        },
        { 
            name: $t.testimonials?.items?.[2]?.name , 
            role: $t.testimonials?.items?.[2]?.role, 
            quote: $t.testimonials?.items?.[2]?.quote  
        }
    ];

    $: faqs = ($t.faq?.items || []).slice(0, 6).map(item => ({
        question: item?.question || '',
        answer: item?.answer || ''
    }));
</script>

<div class="app">
    {#if mounted && !fromStartNow}
        <PublicNavbar currentPage="pricing" />
    {/if}

    <main class="main-content">
        <section class="pricing-section">
            <h1 class="section-title">{$t.pricing?.title || 'Pricing'}</h1>
            
            <div class="pricing-cards">
                <div class="pricing-card">
                    <h2>{$t.pricing?.forAthletes?.title || 'For Athletes'}</h2>
                    <p class="price">{$t.pricing?.forAthletes?.price || '6.96€'}<span>{$t.pricing?.forAthletes?.period || '/month'}</span></p>
                    
                    <button class="cta-button" on:click={handleStartNowClick}>{$t.pricing?.startNow || 'Start now'}</button>
                    
                    <ul class="features-list">
                        {#each ($t.pricing?.forAthletes?.features || []).filter(feature => !feature.toLowerCase().includes('unlimited video uploads')) as feature}
                            <li>{feature}</li>
                        {/each}
                    </ul>
                </div>

                <div class="pricing-card">
                    <h2>{$t.pricing?.forCoaches?.title || 'For Coaches'}</h2>
                    <p class="price-placeholder">Custom pricing for your needs</p>
                    
                    <button class="cta-button contact-us" on:click={handleContactUsClick}>{$t.pricing?.contactUs || 'Contact us'}</button>
                    
                    <ul class="features-list">
                        {#each $t.pricing?.forCoaches?.features || [] as feature}
                            <li>{feature}</li>
                        {/each}
                    </ul>
                </div>
            </div>
        </section>

        <section class="guarantee-section">
            <div class="guarantee-content">
                <Check size={48} color="#efc824" />
                <div>
                    <p>{$t.pricing?.guarantee?.p1 || "If within the next 7 days you feel that Yekar is not for you, simply send me an email to my personal address: jon@yekar.es and I will refund 100% of your money."}</p>
                    <p>{$t.pricing?.guarantee?.p2 || "No questions asked. We will do all that's possible to make sure it is worth it for you. Our money-back guarantee is 100% safe and risk-free."}</p>
                    <p class="signature">{$t.pricing?.guarantee?.signature || 'Jon Galarraga | CEO of Yekar'}</p>
                </div>
            </div>
        </section>

        <Testimonials {testimonials} />

        <FAQ {faqs} />
    </main>
</div>

{#if mounted && !fromStartNow}
    <Footer />
{/if}

<style>
    .main-content {
        max-width: 75rem;
        margin: 0 auto;
        padding: 2.5rem 1.25rem;
    }

    .pricing-section {
        text-align: center;
        padding: 2rem 0;
    }

    .section-title {
        font-size: 3rem;
        font-weight: 900;
        color: #efc824;
        margin-bottom: 1.5rem;
        line-height: 1.2;
        padding: 0 1rem;
    }

    .pricing-cards {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 4rem;
        padding: 0 1rem;
        flex-wrap: wrap;
    }

    .pricing-card {
        background-color: #2a2a2a;
        border-radius: 0.5rem;
        padding: 2rem;
        width: 21.875rem;
        max-width: 100%;
        text-align: left;
        position: relative;
        flex: 1;
        min-width: 280px;
    }

    .pricing-card h2 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: #efc824;
        line-height: 1.2;
    }

    .price {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        line-height: 1.2;
    }

    .price span {
        font-size: 1rem;
        font-weight: normal;
    }

    .cta-button {
        background-color: #efc824;
        color: #000000;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 1.5rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
        width: 100%;
        min-height: 44px;
        font-size: 1rem;
    }

    .cta-button:hover {
        transform: translateY(-0.1875rem);
        box-shadow: 0 0.25rem 0.375rem rgba(0, 0, 0, 0.1);
    }

    .features-list {
        list-style-type: none;
        padding: 0;
    }

    .features-list li {
        margin-bottom: 0.75rem;
        position: relative;
        padding-left: 1.5rem;
        line-height: 1.4;
    }

    .features-list li::before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #efc824;
    }

    .guarantee-section {
        background-color: #2a2a2a;
        border: 0.125rem solid #efc824;
        border-radius: 0.5rem;
        padding: 2rem;
        margin: 0 1rem 4rem 1rem;
    }

    .guarantee-content {
        display: flex;
        align-items: flex-start;
        gap: 1.5rem;
    }

    .guarantee-content p {
        color: #e3e3e3;
        margin-bottom: 1rem;
        line-height: 1.6;
    }

    .signature {
        font-weight: bold;
        color: #efc824;
    }

    .cta-button.contact-us {
        background-color: #2a2a2a;
        color: #efc824;
        border: 2px solid #efc824;
    }

    .cta-button.contact-us:hover {
        background-color: #efc824;
        color: #2a2a2a;
    }

    .price-placeholder {
        font-size: 1.2rem;
        font-style: italic;
        color: #888;
        margin-bottom: 1.5rem;
        line-height: 1.4;
    }

    @media (max-width: 768px) {
        .main-content {
            padding: 1.5rem 1rem;
        }

        .section-title {
            font-size: 2.5rem;
            margin-bottom: 1.25rem;
        }

        .pricing-cards {
            gap: 1.5rem;
            margin-bottom: 3rem;
        }

        .pricing-card {
            padding: 1.5rem;
            min-width: 260px;
        }

        .guarantee-section {
            padding: 1.5rem;
            margin-bottom: 3rem;
        }

        .guarantee-content {
            gap: 1.25rem;
        }
    }

    @media (max-width: 480px) {
        .main-content {
            padding: 1rem 0.5rem;
        }

        .section-title {
            font-size: 2rem;
            margin-bottom: 1rem;
        }

        .pricing-cards {
            gap: 1rem;
            margin-bottom: 2rem;
            padding: 0 0.5rem;
        }

        .pricing-card {
            padding: 1.25rem;
            min-width: 240px;
        }

        .pricing-card h2 {
            font-size: 1.25rem;
        }

        .price {
            font-size: 1.75rem;
        }

        .price-placeholder {
            font-size: 1.1rem;
        }

        .cta-button {
            padding: 0.625rem 1.25rem;
            font-size: 0.95rem;
        }

        .features-list li {
            font-size: 0.95rem;
            margin-bottom: 0.625rem;
        }

        .guarantee-section {
            padding: 1.25rem;
            margin: 0 0.5rem 2rem 0.5rem;
        }

        .guarantee-content {
            flex-direction: column;
            gap: 1rem;
            align-items: center;
            text-align: center;
        }

        .guarantee-content p {
            font-size: 0.95rem;
            margin-bottom: 0.75rem;
        }
    }

    .btn-primary {
        background-color: #efc824;
        color: #000000;
    }

    .btn-primary:hover {
        background-color: #f5d547;
    }
</style>
