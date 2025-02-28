<script>
    //@ts-nocheck
    import { t } from '../i18n.js';
    
    let email = '';
    let password = '';
    let errorMessage = '';
    let isAuthenticated = false;
    let authenticatedEmail = '';
    let subscriptionStatus = '';

    const checkAuthStatus = async () => {
        try {
            const response = await fetch('/api/auth-status/');
            const data = await response.json();
            if (response.ok && data.is_authenticated) {
                isAuthenticated = true;
                authenticatedEmail = data.email;
                subscriptionStatus = data.subscription_status;
                
                if (subscriptionStatus === 'EXPIRED' || subscriptionStatus === 'INACTIVE') {
                    window.location.href = '/account-settings';
                }
            }
        } catch (error) {
            console.error('Error checking auth status:', error);
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

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!email || !password) {
            console.error('Email or password is missing');
            errorMessage = $t.login?.emptyFieldsError || 'Email and password must not be empty';
            return;
        }

        try {
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            const response = await fetch('/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ username: email, password })
            });

            const data = await response.json();
            if (response.ok) {
                window.location.href = '/dashboard';
            } else {
                errorMessage = data.error || ($t.login?.genericError || 'An error occurred');
                console.error('Login error:', errorMessage);
            }
        } catch (error) {
            errorMessage = $t.login?.genericError || 'An error occurred';
            console.error('Fetch error:', error);
        }
    };

    checkAuthStatus();
</script>

<main>
    <div class="left-panel">
        <div class="logo-container">
            <img src="/static/icons/YekarLogo.svg" alt="Yekar-Logo" />
        </div>
    </div>
    <div class="right-panel">
        {#if isAuthenticated && (subscriptionStatus === 'ACTIVE' || subscriptionStatus === 'CANCELLED')}
            <h1>{$t.login?.alreadyLoggedIn || 'You are already logged in'}</h1>
            <p>{$t.login?.loggedInAs || 'You are logged in as'} <strong>{authenticatedEmail}</strong></p>
            <div class="button-container">
                <button class="continue-btn" on:click={() => window.location.href = '/dashboard'}>
                    {$t.login?.continueButton || 'Continue →'}
                </button>
                <button class="logout-btn" on:click={handleLogout}>
                    {$t.login?.logoutButton || 'Logout'}
                </button>
            </div>
        {:else}
            <h1>{$t.login?.title || 'Welcome Back!'}</h1>
            <form on:submit={handleSubmit}>
                <input type="email" id="email" bind:value={email} placeholder={$t.login?.email || 'Email'} required />
                <input type="password" id="password" bind:value={password} placeholder={$t.login?.password || 'Password'} required />

                {#if errorMessage}
                    <p class="error-message">{errorMessage}</p>
                {/if}

                <button type="submit">{$t.login?.submitButton || 'Log In →'}</button>
            </form>
            <p>{@html $t.login?.noAccount || "Don't have an account? <a href='/api/register'>Click here to register</a>."}</p>
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
    }

    .logo-container img {
        height: 4rem;
        width: auto;
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
        background-color: #000000;
        color: #efc824;
        min-height: 44px;
        font-size: 1rem;
    }

    button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(239, 200, 36, 0.2);
    }

    .error-message {
        color: #ff5252;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        padding: 0 1rem;
        text-align: left;
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

    p {
        text-align: center;
        margin-top: 1rem;
        padding: 0 1rem;
        line-height: 1.4;
        color: #000000;
    }

    a {
        color: #000000;
        text-decoration: underline;
        transition: all 0.3s ease;
    }

    a:hover {
        color: #000000;
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
            background-color: #000000;
            color: #e3e3e3;
        }

        h1 {
            color: #efc824;
        }

        p {
            color: #e3e3e3;
        }

        a {
            color: #efc824;
        }

        a:hover {
            color: #ffffff;
        }

        button {
            background-color: #efc824;
            color: #000000;
        }

        .right-panel {
            flex: 1;
            min-height: 100vh;
            padding: 1rem;
            justify-content: flex-start;
            padding-top: 4rem;
        }

        h1 {
            font-size: 2rem;
            margin-bottom: 1.5rem;
        }

        input, button {
            font-size: 0.95rem;
            padding: 0.625rem;
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

        p {
            font-size: 0.9rem;
            padding: 0 0.5rem;
        }
    }
</style>
