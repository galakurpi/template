<script>
  import { AlertTriangle } from 'lucide-svelte';
  import { t } from '../i18n.js';
  import PublicNavbar from '../common/PublicNavbar.svelte';

  const whatsappLink = "https://wa.me/34747405452";
</script>

<PublicNavbar currentPage="cancel" />

<div class="cancel-container">
  <div class="cancel-content">
    <AlertTriangle class="cancel-icon" size={64} />
    <h1 class="cancel-title">{$t.cancel?.title || 'Payment Canceled'}</h1>
    <p class="cancel-message">{@html $t.cancel?.message || 'The payment didn\'t work.<br>Please contact us by email: jon@yekar.es or via WhatsApp'}</p>
    <div class="button-container">
      <a href="mailto:jon@yekar.es" class="btn email-btn">
        {$t.cancel?.emailButton || 'Email'}
      </a>
      <a href={whatsappLink} target="_blank" rel="noopener noreferrer" class="btn whatsapp-btn">
        {$t.cancel?.whatsappButton || 'WhatsApp'}
      </a>
    </div>
  </div>
</div>

<style>
  .cancel-container {
    min-height: calc(100vh - 6rem);
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #000000;
    color: #e3e3e3;
    font-family: 'Montserrat', sans-serif;
    padding: 1rem;
  }

  .cancel-content {
    text-align: center;
    padding: 2.5rem;
    max-width: 600px;
    width: 100%;
  }

  .cancel-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 1.5rem;
    color: #efc824;
    line-height: 1.2;
    padding: 0 1rem;
  }

  .cancel-message {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    line-height: 1.6;
    padding: 0 1rem;
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

  .email-btn:hover,
  .whatsapp-btn:hover {
    transform: scale(1.05);
  }

  @media (max-width: 768px) {
    .cancel-content {
      padding: 2rem 1rem;
    }

    .cancel-title {
      font-size: 2.5rem;
      margin-bottom: 1.25rem;
    }

    .cancel-message {
      font-size: 1.1rem;
      margin-bottom: 1.75rem;
    }

    .btn {
      font-size: 1rem;
      padding: 0.625rem 1.25rem;
    }
  }

  @media (max-width: 480px) {
    .cancel-content {
      padding: 1.5rem 0.5rem;
    }

    .cancel-title {
      font-size: 2rem;
      margin-bottom: 1rem;
    }

    .cancel-message {
      font-size: 1rem;
      margin-bottom: 1.5rem;
    }

    .btn {
      font-size: 0.95rem;
      padding: 0.5rem 1rem;
      min-width: 100px;
    }

    .button-container {
      flex-direction: column;
      width: 100%;
      padding: 0 0.5rem;
    }

    .email-btn,
    .whatsapp-btn {
      max-width: none;
      width: 100%;
    }
  }
</style>
