<script>
  //@ts-nocheck
  import { onMount } from 'svelte';
  import { AlertTriangle, CheckCircle, XCircle, Mail } from 'lucide-svelte';
  import { t } from '../i18n.js';
  import PublicNavbar from '../common/PublicNavbar.svelte';
  let subscriptionStatus = 'loading';
  let message = '';
  let showContactButtons = false;
  let isCanceling = false;
  let userEmail = '';
  let isAthlete = false;
  let isCoach = false;
  let isActivating = false;

  let stripePublishableKey = '';
  let stripe = null;

  const whatsappLink = "https://wa.me/34747405452";

  async function getStripeKey() {
    try {
      const response = await fetch('/api/stripe-key/');
      const data = await response.json();
      stripePublishableKey = data.stripe_publishable_key;

      stripe = (window).Stripe(stripePublishableKey, {
        scriptLoadOptions: {
          crossorigin: 'anonymous',
        },
      });
      console.log('Stripe initialized:', stripe);
    } catch (error) {
      console.error('Error fetching Stripe key:', error);
      message = 'An error occurred while initializing payment system.';
    }
  }

  async function checkAuthStatus() {
    try {
      const response = await fetch('/api/auth-status/');
      const data = await response.json();
      console.log("Check auth status data:", data);
      if (response.ok) {
        if (data.is_authenticated) {
          userEmail = data.email;
          subscriptionStatus = data.subscription_status;
          isAthlete = data.is_athlete;
          isCoach = data.is_coach;
        } else {
          subscriptionStatus = 'NOT_AUTHENTICATED';
          userEmail = null; // Clear email if not authenticated
        }
      } else {
        subscriptionStatus = 'NOT_AUTHENTICATED';
        userEmail = null; // Clear email if not authenticated
        throw new Error('Failed to fetch auth status');
      }
    } catch (error) {
      console.error('Error checking auth status:', error);
      message = $t.accountSettings?.errorMessage || 'An error occurred while fetching account information.';
      showContactButtons = true;
    }
  }


  onMount(async () => {
    await checkAuthStatus();
  });

  async function handleCancelSubscription() {
    isCanceling = true;
    try {
      const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
      const response = await fetch('/api/cancel-subscription/', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
          email: userEmail
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to cancel the subscription');
      }

      const data = await response.json();
      if (data.success) {
        subscriptionStatus = 'CANCELLED';
        message = 'Your account has been cancelled, you can still use the app until your account expires';
      } else {
        message = 'Failed to cancel the account. Please try again later.';
      }
    } catch (error) {
      console.error(error);
      message = 'An error occurred while canceling your account.';
    } finally {
      isCanceling = false;
    }
  }

  async function handleActivateAccount() {
    await getStripeKey();
    isActivating = true;
    try {
      const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
      const response = await fetch('/api/get_checkout_session_for_registered/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ product_type: 'monthly' }) 
      });

      if (!response.ok) {
        throw new Error('Failed to create checkout session');
      }

      const data = await response.json();
      if (data.sessionId) {
        // Redirect to Stripe Checkout
        const result = await stripe.redirectToCheckout({ sessionId: data.sessionId });
        if (result.error) {
          throw new Error(result.error.message);
        }
      } else {
        throw new Error('No session ID returned');
      }
    } catch (error) {
      console.error(error);
      message = 'An error occurred while activating your account. Please try again later.';
    } finally {
      isActivating = false;
    }
  }

  async function handleLogout() {
    try {
      const response = await fetch('/api/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        }
      });
      if (response.ok) {
        // Clear all cache
        localStorage.clear();
        sessionStorage.clear();
        document.cookie.split(";").forEach(function(c) { 
          document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
        });

        // Clear application cache if supported by the browser
        if ('caches' in window) {
          caches.keys().then(function(names) {
            for (let name of names)
              caches.delete(name);
          });
        }

        // Redirect to login page
        window.location.href = '/api/login/';
      } else {
        console.error('Logout failed');
      }
    } catch (error) {
      console.error('Logout error:', error);
    }
  }

  async function handleDeleteAccount() {
    if (!confirm($t.accountSettings?.deleteAccount?.confirmMessage || 'Are you sure you want to delete your account? This action cannot be undone.')) {
      return;
    }

    try {
      const csrfToken = document.querySelector("meta[name='csrf-token']").getAttribute("content");
      const response = await fetch('/api/delete-account/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        }
      });

      if (!response.ok) {
        throw new Error('Failed to delete account');
      }

      // If successful, clear everything and redirect to login
      localStorage.clear();
      sessionStorage.clear();
      document.cookie.split(";").forEach(function(c) { 
        document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
      });

      window.location.href = '/api/login/';
    } catch (error) {
      console.error('Delete account error:', error);
      message = 'An error occurred while deleting your account. Please try again later.';
    }
  }
</script>

<PublicNavbar currentPage="account" />

<div class="account-container">
  <div class="account-content">
    {#if userEmail}
      <div class="email-container">
        <Mail class="email-icon" size={24} />
        <span class="email-text">{userEmail}</span>
      </div>
    {/if}

    {#if subscriptionStatus === 'ACTIVE'}
      <div class="upper-section">
        <h2 class="contact-title">{$t.accountSettings?.contactTitle || 'Contact us'}</h2>
        <div class="button-container">
          <a href="mailto:jon@yekar.es" class="btn email-btn">
            {$t.accountSettings?.emailButton || 'Email'}
          </a>
          <a href={whatsappLink} target="_blank" rel="noopener noreferrer" class="btn whatsapp-btn">
            {$t.accountSettings?.whatsappButton || 'WhatsApp'}
          </a>
        </div>
      </div>

      <div class="lower-section">
        <div class="status-container ACTIVE">
          <CheckCircle class="status-icon" size={24} />
          <span>{$t.accountSettings?.activeStatus || 'Your account is active'}</span>
        </div>
        <div class="action-buttons">
          <button class="btn cancel-btn" on:click={handleCancelSubscription} disabled={isCanceling}>
            {#if isCanceling}
              {$t.accountSettings?.cancellingButton || 'Cancelling...'}
            {:else}
              {$t.accountSettings?.cancelAccountButton || 'Cancel account'}
            {/if}
          </button>
          <button class="btn logout-btn" on:click={handleLogout}>
            {$t.nav?.logout || 'LOG OUT'}
          </button>
          <button class="btn delete-btn" on:click={handleDeleteAccount}>
            Delete Account
          </button>
        </div>
      </div>
    {:else if subscriptionStatus === 'NOT_AUTHENTICATED'}
      <div class="upper-section">
        <div class="status-container NOT_AUTHENTICATED">
          <XCircle class="status-icon" size={24} />
          <span>{$t.accountSettings?.notAuthenticatedStatus || 'You are not authenticated'}</span>
        </div>
        <button class="btn activate-btn create-account-btn" on:click={() => window.location.href = '/register'}>
          {$t.accountSettings?.createAccountButton || 'Create account'}
        </button>
      </div>

    {:else}
      {#if subscriptionStatus === 'CANCELLED' }
        <div class="upper-section">
          <div class="status-container CANCELLED">
            <XCircle class="status-icon" size={24} />
            <span>{$t.accountSettings?.cancelledStatus || 'Your account has been cancelled, you can still use the app until your account expires'}</span>
          </div>
        </div>
      {:else if subscriptionStatus === 'EXPIRED'}
        <div class="upper-section">
          <div class="status-container EXPIRED">
            <XCircle class="status-icon" size={24} />
            <span>{$t.accountSettings?.expiredStatus || 'Your subscription has expired'}</span>
          </div>
        </div>
      {/if}

      <div class="lower-section">
        <div class="action-buttons">
          <button class="btn activate-btn" on:click={handleActivateAccount} disabled={isActivating}>
            {#if isActivating}
              {$t.accountSettings?.activatingButton || 'Activating...'}
            {:else}
              {$t.accountSettings?.activateButton || 'Activate account'}
            {/if}
          </button>
          <button class="btn logout-btn" on:click={handleLogout}>
            {$t.nav?.logout || 'LOG OUT'}
          </button>
          {#if userEmail}
            <button class="btn delete-btn" on:click={handleDeleteAccount}>
              Delete Account
            </button>
          {/if}
        </div>
      </div>

    {/if}

    {#if message}
      <div class="message-container">
        <AlertTriangle class="message-icon" size={24} />
        <p>{message}</p>
      </div>
    {/if}

    {#if subscriptionStatus !== 'ACTIVE'}
      <div class="lower-section">
        <h2 class="contact-title">{$t.accountSettings?.contactTitle || 'Contact us'}</h2>
        <div class="button-container">
          <a href="mailto:jon@yekar.es" class="btn email-btn">
            {$t.accountSettings?.emailButton || 'Email'}
          </a>
          <a href={whatsappLink} target="_blank" rel="noopener noreferrer" class="btn whatsapp-btn">
            {$t.accountSettings?.whatsappButton || 'WhatsApp'}
          </a>
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  .account-container {
    min-height: calc(100vh - 6rem);
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #000000;
    color: #e3e3e3;
    font-family: 'Montserrat', sans-serif;
    padding: 1rem;
  }

  .account-content {
    text-align: center;
    padding: 2.5rem;
    max-width: 600px;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: calc(100vh - 6rem - 80px);
    gap: 1.5rem;
  }

  .upper-section {
    margin-bottom: 2rem;
  }

  .lower-section {
    margin-top: 2rem;
  }

  .status-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5rem;
    font-size: 1.2rem;
    gap: 0.75rem;
    padding: 0 1rem;
    line-height: 1.4;
    flex-wrap: wrap;
  }

  .message-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5rem;
    font-size: 1.1rem;
    color: #efc824;
    gap: 0.75rem;
    padding: 0 1rem;
    line-height: 1.4;
    flex-wrap: wrap;
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
    min-height: 44px;
    min-width: 120px;
  }

  .button-container {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
    padding: 0 1rem;
  }

  .email-btn,
  .whatsapp-btn {
    background-color: #e3e3e3;
    color: #000000;
    flex: 1;
    max-width: 200px;
  }

  .create-account-btn {
    margin-bottom: 1.5rem;
    width: 100%;
    max-width: 300px;
  }

  .cancel-btn {
    background-color: transparent;
    color: #808080;
    border: 1px solid #808080;
    font-size: 0.9rem;
    padding: 0.75rem 1.5rem;
    margin-top: 1.25rem;
    width: 100%;
    max-width: 300px;
  }

  .cancel-btn:hover {
    background-color: rgba(128, 128, 128, 0.1);
  }

  .cancel-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .email-btn:hover,
  .whatsapp-btn:hover,
  .cancel-btn:hover {
    transform: scale(1.05);
  }

  .activate-btn {
    background-color: #4CAF50;
    color: #ffffff;
    width: 100%;
    max-width: 300px;
  }

  .activate-btn:hover {
    transform: scale(1.05);
  }

  .email-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 3rem;
    font-size: 1.1rem;
    color: #e3e3e3;
    gap: 0.75rem;
    padding: 0 1rem;
  }

  .email-text {
    font-weight: 600;
    word-break: break-all;
  }

  .activate-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .contact-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    color: #efc824;
    padding: 0 1rem;
    line-height: 1.2;
  }

  .action-buttons {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .logout-btn {
    background-color: #2a2a2a;
    color: #efc824;
    border: 2px solid #efc824;
    width: 100%;
    max-width: 300px;
  }

  .logout-btn:hover {
    background-color: #efc824;
    color: #2a2a2a;
    transform: scale(1.05);
  }

  .delete-btn {
    background-color: #dc3545;
    color: #ffffff;
    border: none;
    width: 100%;
    max-width: 300px;
    margin-top: 1rem;
  }

  .delete-btn:hover {
    background-color: #c82333;
    transform: scale(1.05);
  }

  @media (max-width: 768px) {
    .account-content {
      padding: 2rem 1rem;
    }

    .btn {
      font-size: 1rem;
      padding: 0.625rem 1.25rem;
    }

    .contact-title {
      font-size: 1.25rem;
    }

    .status-container,
    .message-container {
      font-size: 1rem;
    }
  }

  @media (max-width: 480px) {
    .account-content {
      padding: 1.5rem 0.5rem;
    }

    .btn {
      font-size: 0.95rem;
      padding: 0.5rem 1rem;
      min-width: 100px;
    }

    .email-btn,
    .whatsapp-btn {
      max-width: none;
      width: 100%;
    }

    .button-container {
      flex-direction: column;
      width: 100%;
      padding: 0 0.5rem;
    }

    .status-container,
    .message-container {
      font-size: 0.95rem;
      text-align: center;
    }

    .email-container {
      font-size: 0.95rem;
      flex-wrap: wrap;
      justify-content: center;
      text-align: center;
      margin-bottom: 2rem;
    }
  }
</style>
