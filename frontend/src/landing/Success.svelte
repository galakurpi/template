<script lang="ts">
    import { onMount } from 'svelte';
    import { CheckCircle, Loader, AlertTriangle } from 'lucide-svelte';
    import { t } from '../i18n.js';
    import PublicNavbar from '../common/PublicNavbar.svelte';

    let processing = true;
    let success = false;
    let error = false;
    let message = '';
    let session_id: string | null = '';
    let retryCount = 0;
    const maxRetries = 15;
    const retryInterval = 2000;

    const whatsappLink = "https://wa.me/34747405452";

    onMount(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const sessionParam = urlParams.get('session_id');

        if (!sessionParam) {
            error = true;
            message = 'No session ID provided.';
            processing = false;
        } else {
            session_id = sessionParam;
            checkStatus();
        }
    });

    const checkStatus = async () => {
        if (!session_id) {
            error = true;
            message = 'No session ID available.';
            processing = false;
            return;
        }

        if (retryCount >= maxRetries) {
            error = true;
            message = 'Payment processing is taking longer than expected. Please check your payment method or contact support for assistance.';
            processing = false;
            return;
        }
        retryCount++;

        try {
            const response = await fetch(`/api/check_payment_status/?session_id=${session_id}`);
            if (response.ok) {
                const data = await response.json();
                console.log('Payment status response:', data);
                
                if (data.status === 'completed') {
                    success = true;
                    processing = false;
                } else if (data.status === 'pending') {
                    setTimeout(checkStatus, retryInterval);
                } else if (data.status === 'error') {
                    error = true;
                    message = data.message || 'Your payment could not be processed. Please try again or contact support.';
                    processing = false;
                }
            } else {
                const errorData = await response.json();
                console.error('Payment status error:', errorData);
                error = true;
                message = errorData.message || 'An error occurred while checking payment status. Please contact support.';
                processing = false;
            }
        } catch (err) {
            console.error('Payment status check error:', err);
            error = true;
            message = 'An error occurred while checking payment status. Please try again or contact support.';
            processing = false;
        }
    };
</script>

<PublicNavbar currentPage="landing" />

<div class="container">
    {#if processing}
        <div class="content">
            <Loader class="icon" size={64} />
            <h1 class="title">Processing your payment...</h1>
            <p class="message">Please wait while we confirm your subscription.</p>
        </div>
    {:else if success}
        <div class="content">
            <CheckCircle class="icon success-icon" size={64} />
            <h1 class="title success-title">{$t.success?.title || 'Welcome!'}</h1>
            <p class="message">{@html $t.success?.message || 'Thank you for using Yekar.<br>You can now log in to your account.'}</p>
            <a href="/api/login" class="btn login-btn">
                {$t.success?.loginButton || 'Log In'}
            </a>
        </div>
    {:else if error}
        <div class="content">
            <AlertTriangle class="icon error-icon" size={64} />
            <h1 class="title error-title">An error occurred</h1>
            <p class="message error-message">{message}</p>
            <p>Please contact support for assistance.</p>
            <div class="button-container">
                <a href="mailto:jon@yekar.es" class="btn email-btn">
                    {$t.cancel?.emailButton || 'Email'}
                </a>
                <a href={whatsappLink} target="_blank" rel="noopener noreferrer" class="btn whatsapp-btn">
                    {$t.cancel?.whatsappButton || 'WhatsApp'}
                </a>
            </div>
        </div>
    {/if}
</div>

<style>
    .container {
        min-height: calc(100vh - 6rem);
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #000000;
        color: #e3e3e3;
        font-family: 'Montserrat', sans-serif;
        padding: 1rem;
    }

    .content {
        text-align: center;
        padding: 2.5rem;
        max-width: 600px;
        width: 100%;
    }

    .title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        line-height: 1.2;
        padding: 0 1rem;
    }

    .message {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        line-height: 1.6;
        padding: 0 1rem;
    }

    .success-title {
        color: #4CAF50;
    }

    .error-title {
        color: #FF5252;
    }

    .btn {
        padding: 0.75rem 1.5rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 1.1rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        border: none;
        text-decoration: none;
        margin: 0 0.5rem;
        min-height: 44px;
        min-width: 120px;
    }

    .login-btn {
        background-color: #4CAF50;
        color: #ffffff;
        width: 100%;
        max-width: 300px;
    }

    .button-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1.5rem;
        flex-wrap: wrap;
        padding: 0 1rem;
    }

    .email-btn {
        background-color: #e3e3e3;
        color: #000000;
        flex: 1;
        max-width: 200px;
    }

    .whatsapp-btn {
        background-color: #25D366;
        color: #ffffff;
        flex: 1;
        max-width: 200px;
    }

    .login-btn:hover,
    .email-btn:hover,
    .whatsapp-btn:hover {
        transform: scale(1.05);
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    :global(.icon) {
        margin-bottom: 1.5rem;
    }

    :global(.success-icon) {
        color: #4CAF50;
    }

    :global(.error-icon) {
        color: #FF5252;
    }

    :global(.icon.loader) {
        animation: spin 1s linear infinite;
    }

    @media (max-width: 768px) {
        .content {
            padding: 2rem 1rem;
        }

        .title {
            font-size: 2.5rem;
            margin-bottom: 1.25rem;
        }

        .message {
            font-size: 1.1rem;
            margin-bottom: 1.75rem;
        }

        .btn {
            font-size: 1rem;
            padding: 0.625rem 1.25rem;
        }

        :global(.icon) {
            margin-bottom: 1.25rem;
        }
    }

    @media (max-width: 480px) {
        .content {
            padding: 1.5rem 0.5rem;
        }

        .title {
            font-size: 2rem;
            margin-bottom: 1rem;
        }

        .message {
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }

        .btn {
            font-size: 0.95rem;
            padding: 0.5rem 1rem;
            min-width: 100px;
            margin: 0;
        }

        .button-container {
            flex-direction: column;
            width: 100%;
            padding: 0 0.5rem;
            gap: 0.75rem;
        }

        .email-btn,
        .whatsapp-btn {
            max-width: none;
            width: 100%;
        }

        .login-btn {
            width: 100%;
            max-width: none;
        }

        :global(.icon) {
            margin-bottom: 1rem;
            transform: scale(0.9);
        }
    }
</style>
