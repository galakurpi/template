<script>
  import { Instagram, Twitter, Youtube } from 'lucide-svelte';
  import { t } from '../i18n.js';  // Import the translation store

  const currentYear = new Date().getFullYear();
</script>

<footer>
  <div class="footer-content">
    <div class="footer-main">
      <div class="logo-and-social">
        <div class="logo-holder">
          <img src="/static/icons/YekarLogo.svg" alt="Yekar-Logo" />
        </div>
        <div class="social-links">
          <a href={$t.footer?.socialLinks?.instagram || "https://www.instagram.com/yekar_en"} target="_blank" rel="noopener noreferrer">
            <Instagram size={24} />
          </a>
          <a href={$t.footer?.socialLinks?.twitter || "https://twitter.com/yekar_ai"} target="_blank" rel="noopener noreferrer">
            <Twitter size={24} />
          </a>
          <a href={$t.footer?.socialLinks?.youtube || "https://www.youtube.com/@yekar_en"} target="_blank" rel="noopener noreferrer">
            <Youtube size={24} />
          </a>
          <a href={$t.footer?.socialLinks?.tiktok || "https://www.tiktok.com/@yekar_en"} target="_blank" rel="noopener noreferrer">
            {$t.footer?.tiktok || 'Tiktok'}
          </a>
        </div>
      </div>
      <div class="legal-links">
        <a href="/privacy-policy">{$t.footer?.legalLinks?.privacyPolicy || 'Privacy Policy'}</a>
        <a href="/cookie-policy">{$t.footer?.legalLinks?.cookiePolicy || 'Cookie Policy'}</a>
        <a href="/terms-of-service">{$t.footer?.legalLinks?.termsOfService || 'Terms of Service'}</a>
      </div>
    </div>
  </div>
  <!-- <p class="copyright">{$t.footer?.copyright?.replace('{year}', currentYear) || `Yekar © ${currentYear}. All rights reserved.`}</p> -->
</footer>

<style>
  footer {
    background-color: #000000;
    color: #ffffff;
    padding: 2rem 0;
    margin-top: 2rem;
  }

  .footer-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
  }

  .footer-main {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5rem;
  }

  .logo-and-social {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .logo-holder img {
    height: 2.5rem;
    width: auto;
  }

  .social-links {
    display: flex;
    gap: 1rem;
  }

  .social-links a {
    color: #ffffff;
    transition: color 0.3s ease;
  }

  .social-links a:hover {
    color: #efc824;
  }

  .legal-links {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }

  .legal-links a {
    color: #ffffff;
    text-decoration: none;
    font-size: 0.9rem;
  }

  .legal-links a:hover {
    text-decoration: underline;
  }


  @media (max-width: 767px) {
    .footer-main {
      flex-direction: column;
      gap: 2rem;
    }

    .legal-links {
      align-items: center;
    }
  }
</style>
