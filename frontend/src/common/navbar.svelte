<script lang="ts">
    //@ts-nocheck
    import { createEventDispatcher, onMount } from "svelte";
    import { t } from '../i18n';  // Import the translation store
    import { User } from 'lucide-svelte';  // Import the User icon

  const dispatch = createEventDispatcher();
  let currentPath = "";

  function handleMenuClick() {
    dispatch("toggle-menu");
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

  function handleDashboardClick() {
    if (currentPath !== "/dashboard") {
      window.location.href = "/dashboard";
    } else {
      window.location.href = "/prototype";
    }
  }

  function handleLogoClick() {
    window.location.href = "/prototype";
  }

  function handleAccountSettingsClick() {
    window.location.href = "/account-settings";
  }

  onMount(() => {
    currentPath = window.location.pathname;
  });
</script>

<nav>
  <div class="left-buttons">
    {#if currentPath !== "/login"}
      <button on:click={handleDashboardClick} class="dashboard-button">
        {currentPath !== "/dashboard" ? $t.nav?.dashboard || 'Dashboard' : $t.nav?.upload || 'Upload'}
      </button>
    {/if}
  </div>
  <div class="logo-holder" on:click={handleLogoClick}>
    <img src="/static/icons/YekarLogo.svg" alt="TSG-Logo" />
  </div>
  <div class="settings-holder">
    <button on:click={handleAccountSettingsClick} class="account-button" title={$t.nav?.accountSettings || 'Account Settings'}>
      <User size={24} />
    </button>
    <button on:click={handleLogout} class="logout-button">{$t.nav?.logout || 'LOG OUT'}</button>
  </div>
</nav>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Proxima+Nova:wght@400&display=swap');

  nav {
    background-color: #000000;
    min-height: 4rem;
    height: auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 2rem;
    color: #2f2f2f;
    font-family: 'Proxima Nova', sans-serif;
    text-transform: uppercase;
    z-index: 1000;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .left-buttons {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 1rem;
    flex: 1;
    min-width: 200px;
  }

  .logo-holder {
    display: flex;
    justify-content: center;
    align-items: center;
    flex: 1;
    cursor: pointer;
    min-width: 150px;
  }

  .logo-holder img {
    height: 2.5rem;
    width: auto;
    max-width: 100%;
  }

  .settings-holder {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 1rem;
    flex: 1;
    min-width: 200px;
  }

  .dashboard-button, .logout-button {
    background-color: transparent;
    padding: 0.5rem 1rem;
    cursor: pointer;
    font-size: 1rem;
    border: none;
    text-transform: uppercase;
    position: relative;
    font-weight: 600;
    min-width: 44px;
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .dashboard-button {
    color: #e3e3e3;
  }

  .logout-button {
    color: #ed2426;
  }

  .dashboard-button::after, .logout-button::after {
    content: "";
    display: block;
    width: 0;
    height: 3px;
    position: absolute;
    bottom: -3px;
    left: 0;
    transition: width 0.3s;
  }

  .dashboard-button::after {
    background-color: #efc824;
  }

  .logout-button::after {
    background-color: #ed2426;
  }

  .dashboard-button:hover::after, .logout-button:hover::after {
    width: 100%;
  }

  .account-button {
    background-color: transparent;
    color: #e3e3e3;
    padding: 0.5rem;
    cursor: pointer;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: color 0.3s ease;
    min-width: 44px;
    min-height: 44px;
  }

  .account-button:hover {
    color: #efc824;
  }

  @media (max-width: 768px) {
    nav {
      padding: 0.5rem 1rem;
      gap: 0.5rem;
    }

    .left-buttons, .settings-holder {
      min-width: 150px;
      gap: 0.5rem;
    }

    .logo-holder {
      min-width: 120px;
    }

    .logo-holder img {
      height: 2rem;
    }

    .dashboard-button, .logout-button {
      font-size: 0.9rem;
      padding: 0.4rem 0.8rem;
    }
  }

  @media (max-width: 480px) {
    nav {
      padding: 0.5rem;
      justify-content: center;
    }

    .left-buttons, .settings-holder, .logo-holder {
      flex: 0 1 100%;
      justify-content: center;
      min-width: unset;
    }

    .logo-holder {
      order: -1;
    }

    .dashboard-button, .logout-button {
      font-size: 0.85rem;
      padding: 0.3rem 0.6rem;
    }
  }
</style>
