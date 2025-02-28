<script lang="ts">
    import { onMount } from 'svelte';
    import { t } from '../i18n.js';
    import LanguageSwitch from '../common/LanguageSwitch.svelte';
    
    let isAuthenticated = false;
    let authenticatedEmail = '';
    let subscriptionStatus = '';
    
    let firstName = '';
    let lastName = '';
    let email = '';
    let password = '';
    let repeatPassword = '';
    let productType = 'monthly';  
    let errorMessage = '';
    let consentGiven = false;
    let videoConsentGiven = false;
    let phoneNumber = '';
    let instagramHandle = '';
    let affiliateCode = '';

    // Function to get cookie by name
    function getCookie(name: string): string | null {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
        return null;
    }

    // Function to set cookie
    function setCookie(name: string, value: string, days: number = 1) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = `expires=${date.toUTCString()}`;
        document.cookie = `${name}=${value};${expires};path=/`;
    }

    let stripePublishableKey = '';
    let stripe: any = null;

    const getStripeKey = async () => {
        const response = await fetch('/api/stripe-key/');
        const data = await response.json();
        stripePublishableKey = data.stripe_publishable_key;

        // Use the global Stripe object
        stripe = (window as any).Stripe(stripePublishableKey, {
            scriptLoadOptions: {
                crossorigin: 'anonymous',
            },
        });
        console.log('Stripe initialized:', stripe);
    };
    
    const checkAuthStatus = async () => {
        try {
            const response = await fetch('/api/auth-status/');
            const data = await response.json();
            console.log('Auth status response:', data);
            if (response.ok && data.is_authenticated) {
                isAuthenticated = true;
                authenticatedEmail = data.email;
                subscriptionStatus = data.subscription_status;
                
                if (subscriptionStatus === 'EXPIRED' || subscriptionStatus === 'INACTIVE') {
                    window.location.href = '/account-settings';
                } 
            }
            else {
                isAuthenticated = false;
            }
        } catch (error) {
            console.error('Error checking auth status:', error);
        }
    };
    
    onMount(async () => {
        await checkAuthStatus();
        if (!isAuthenticated) {
            await getStripeKey();
            
            // Check URL for affiliate code first
            const urlParams = new URLSearchParams(window.location.search);
            const urlAffiliateCode = urlParams.get('ref');
            
            if (urlAffiliateCode) {
                // If found in URL, update cookie
                setCookie('affiliate_code', urlAffiliateCode);
                affiliateCode = urlAffiliateCode;
                console.log('Affiliate code from URL stored in cookie:', affiliateCode);
            } else {
                // If not in URL, check cookie
                const cookieAffiliateCode = getCookie('affiliate_code');
                if (cookieAffiliateCode) {
                    affiliateCode = cookieAffiliateCode;
                    console.log('Affiliate code found in cookie:', affiliateCode);
                }
            }
        }
    });

    const handleSubmit = async (event: Event) => {
        event.preventDefault();
        if (!consentGiven) {
            errorMessage = $t.register?.consentError || 'You must agree to our policies to register.';
            return;
        }

        if (password !== repeatPassword) {
            errorMessage = $t.register?.errors?.passwordsDoNotMatch || 'Passwords do not match.';
            return;
        }

        if (!productType) {
            errorMessage = $t.register?.errors?.selectSubscription || 'Please select a subscription type.';
            return;
        }

        try {
            const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
            if (!csrfTokenElement) {
                throw new Error('CSRF token not found');
            }
            const csrfToken = csrfTokenElement.getAttribute('content');
            if (!csrfToken) {
                throw new Error('CSRF token is empty');
            }

            // Get affiliate code from cookie if not already set
            if (!affiliateCode) {
                affiliateCode = getCookie('affiliate_code') || '';
            }

            const response = await fetch('/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    first_name: firstName,
                    last_name: lastName,
                    email: email,
                    password: password,
                    product_type: productType,  
                    consent_given: consentGiven,
                    video_consent_given: videoConsentGiven,
                    phone_number: phoneNumber,
                    instagram_handle: instagramHandle,
                    affiliate_code: affiliateCode
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Registration failed');
            }

            const data = await response.json();
            console.log('Registration successful:', data);

            // Clear affiliate cookie after successful registration
            document.cookie = 'affiliate_code=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';

            // Redirect to Stripe checkout page using sessionId
            stripe.redirectToCheckout({ sessionId: data.sessionId });
            
        } catch (error) {
            console.error('Registration error:', error);
            if (error instanceof Error) {
                errorMessage = error.message || $t.register?.errors?.registrationFailed || 'Registration failed';
            } else {
                errorMessage = $t.register?.errors?.unknownError || 'An unknown error occurred';
            }
        }
    };

    const handleLogout = async () => {
        try {
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            const response = await fetch('/api/logout/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });
            if (response.ok) {
                window.location.reload();
            }
        } catch (error) {
            console.error('Logout error:', error);
        }
    };

    function handleLogoClick() {
        window.location.href = "/landing";
    }
</script>


<main>
    <div class="language-switch-container">
        <LanguageSwitch />
    </div>
    <div class="left-panel">
        <div 
            class="logo-container" 
            on:click={handleLogoClick}
            on:keydown={(e) => e.key === 'Enter' && handleLogoClick()}
            tabindex="0"
            role="button"
        >
            <img src="/static/icons/YekarLogo.svg" alt="Yekar-Logo" />
        </div>
        <p>{@html $t.register?.alreadyHaveAccount || "Already have an account? <a href=\"/api/login\">Click here to log in</a>."}</p>
    </div>
    <div class="right-panel">
        {#if isAuthenticated && (subscriptionStatus === 'ACTIVE' || subscriptionStatus === 'CANCELLED')}
            <h1>{$t.register?.alreadyRegistered || 'You are already registered'}</h1>
            <p>{$t.register?.loggedInAs || 'You are logged in as'} <strong>{authenticatedEmail}</strong></p>
            <div class="button-container">
                <button class="continue-btn" on:click={() => window.location.href = '/dashboard'}>
                    {$t.register?.continueButton || 'Continue to Dashboard →'}
                </button>
                <button class="logout-btn" on:click={handleLogout}>
                    {$t.register?.logoutButton || 'Logout'}
                </button>
            </div>
        {:else}
            <h1>{$t.register?.title || "Join Us!"}</h1>
            <form on:submit={handleSubmit}>
                <input type="text" id="firstName" bind:value={firstName} placeholder={$t.register?.firstName || "First Name"} required />
                <input type="text" id="lastName" bind:value={lastName} placeholder={$t.register?.lastName || "Last Name"} required />
                <input type="email" id="email" bind:value={email} placeholder={$t.register?.email || "Email"} required />
                <input type="password" id="password" bind:value={password} placeholder={$t.register?.password || "Password"} required />
                <input type="password" id="repeatPassword" bind:value={repeatPassword} placeholder={$t.register?.repeatPassword || "Repeat Password"} required />
                
                <p class="optional-fields-description">{$t.register?.optionalFieldsDescription || "Add your phone number or Instagram handle so we can help you personally."}</p>
                <input type="tel" id="phoneNumber" bind:value={phoneNumber} placeholder={$t.register?.phoneNumber || "Phone Number (optional)"} />
                <input type="text" id="instagramHandle" bind:value={instagramHandle} placeholder={$t.register?.instagramHandle || "Instagram Handle (optional)"} />
                
                <div class="consent-checkbox">
                    <input type="checkbox" id="consent" bind:checked={consentGiven} required />
                    <label for="consent">
                        {@html $t.register?.combinedConsentLabel || "I agree to the <a href='/privacy-policy' target='_blank'>Privacy Policy</a>, <a href='/terms-of-service' target='_blank'>Terms of Service</a>, by accepting, I also consent to temporary video storage as described (necessary for the service) in the <a href='/privacy-policy#video-storage' target='_blank'>Video Storage Policy</a>."}
                    </label>
                </div>

                {#if errorMessage}
                    <p class="error-message">{errorMessage}</p>
                {/if}

                <button type="submit">{$t.register?.submitButton || "Register with Email →"}</button>
            </form>
        {/if}
    </div>
</main>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@1,900&display=swap');

    main {
        display: flex;
        min-height: 100vh;
        font-family: 'Proxima Nova', sans-serif;
        flex-direction: row;
        background-color: #000000;
    }

    .left-panel {
        flex: 3;
        background-color: #000000;
        color: #e3e3e3;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }

    .logo-container {
        margin-bottom: 2rem;
        cursor: pointer;
    }

    .logo-container img {
        height: 4rem;
        width: auto;
    }

    .left-panel p {
        text-align: center;
        padding: 0 1rem;
        line-height: 1.4;
        color: #e3e3e3;
    }

    .left-panel a {
        color: #efc824;
        text-decoration: underline;
        transition: all 0.3s ease;
    }

    .left-panel a:hover {
        color: #ffffff;
    }

    .right-panel {
        flex: 2;
        background-color: #efc824;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 2rem;
        color: #000000;
    }

    h1 {
        font-family: 'Montserrat', sans-serif;
        font-size: 2.5rem;
        font-weight: 900;
        font-style: italic;
        color: #000000;
        margin-bottom: 2rem;
        text-align: center;
        line-height: 1.2;
        padding: 0 1rem;
    }

    form {
        width: 100%;
        max-width: 400px;
        padding: 0 1rem;
    }

    input {
        width: 100%;
        padding: 0.75rem;
        margin-bottom: 1rem;
        border: 2px solid #2a2a2a;
        border-radius: 8px;
        background-color: #2a2a2a;
        color: #ffffff;
        min-height: 44px;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    input:focus {
        border-color: #efc824;
        outline: none;
    }

    button {
        width: 100%;
        padding: 0.75rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease;
        min-height: 44px;
        font-size: 1rem;
    }

    button[type="submit"] {
        background-color: #000000;
        color: #efc824;
    }

    button[type="submit"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(239, 200, 36, 0.2);
    }

    .consent-checkbox {
        display: flex;
        align-items: flex-start;
        margin-bottom: 1rem;
        gap: 0.75rem;
        padding: 0 1rem;
    }

    .consent-checkbox input[type="checkbox"] {
        margin: 0;
        width: auto;
        min-width: 20px;
        min-height: 20px;
        cursor: pointer;
        accent-color: #efc824;
    }

    .consent-checkbox label {
        font-size: 0.9rem;
        color: #000000;
        line-height: 1.4;
    }

    .consent-checkbox label a {
        color: #000000;
        text-decoration: underline;
        transition: all 0.3s ease;
    }

    .consent-checkbox label a:hover {
        color: #000000;
    }

    .error-message {
        color: #ff5252;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        padding: 0 1rem;
        text-align: left;
    }

    .optional-fields-description {
        font-size: 0.9rem;
        color: #000000;
        margin-bottom: 1rem;
        padding: 0 1rem;
        line-height: 1.4;
    }

    .language-switch-container {
        position: absolute;
        top: 1rem;
        left: 1rem;
        z-index: 10;
    }

    .button-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        width: 100%;
        max-width: 400px;
        padding: 0 1rem;
    }

    .continue-btn, .logout-btn {
        width: 100%;
        padding: 0.75rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease;
        min-height: 44px;
    }

    .continue-btn {
        background-color: #000000;
        color: #efc824;
    }

    .logout-btn {
        background-color: transparent;
        color: #ff5252;
        border: 2px solid #ff5252;
    }

    .continue-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(27, 27, 27, 0.2);
    }

    .logout-btn:hover {
        background-color: #ff5252;
        color: #ffffff;
    }

    @media (max-width: 768px) {
        main {
            flex-direction: column;
            background-color: #000000;
        }

        .left-panel {
            display: none;
        }

        .right-panel {
            flex: 1;
            min-height: 100vh;
            padding: 1rem;
            justify-content: flex-start;
            padding-top: 4rem;
            background-color: #000000;
            color: #e3e3e3;
        }

        h1 {
            font-size: 2rem;
            margin-bottom: 1.5rem;
            color: #efc824;
        }

        input, button {
            font-size: 0.95rem;
            padding: 0.625rem;
        }

        .consent-checkbox label {
            font-size: 0.85rem;
            color: #e3e3e3;
        }

        .consent-checkbox label a {
            color: #efc824;
        }

        .consent-checkbox label a:hover {
            color: #ffffff;
        }

        .language-switch-container {
            top: 0.5rem;
            left: 0.5rem;
        }

        .optional-fields-description {
            color: #e3e3e3;
        }

        .continue-btn {
            background-color: #efc824;
            color: #000000;
        }

        .continue-btn:hover {
            box-shadow: 0 4px 6px rgba(239, 200, 36, 0.2);
        }
    }

    @media (max-width: 480px) {
        .right-panel {
            padding: 0.5rem;
            padding-top: 3.5rem;
        }

        h1 {
            font-size: 1.75rem;
            margin-bottom: 1.25rem;
        }

        form, .button-container {
            padding: 0 0.5rem;
        }

        input, button {
            font-size: 0.9rem;
            padding: 0.5rem;
        }

        .error-message {
            font-size: 0.85rem;
            padding: 0 0.5rem;
        }

        .optional-fields-description {
            font-size: 0.85rem;
            padding: 0 0.5rem;
        }

        .consent-checkbox {
            padding: 0 0.5rem;
        }

        .consent-checkbox label {
            font-size: 0.8rem;
        }

        .left-panel p {
            font-size: 0.9rem;
            padding: 0 0.5rem;
        }
    }
</style>
