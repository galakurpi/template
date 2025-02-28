<script>
    import PublicNavbar from '../common/PublicNavbar.svelte';
    import Footer from '../common/footer.svelte';
    import { t } from '../i18n.js';  // Import the translation store
</script>

<div class="app">
    <PublicNavbar currentPage="cookie-policy" />

    <main class="main-content">
        <h1 class="page-title">{$t.cookiePolicy?.title}</h1>

        <section>
            <h2>{$t.cookiePolicy?.info.title}</h2>
            <p>{$t.cookiePolicy?.info.p1}</p>
        </section>

        <section>
            <h2>{$t.cookiePolicy?.what.title}</h2>
            <p>{$t.cookiePolicy?.what.p1}</p>
            <p>{$t.cookiePolicy?.what.p2}</p>
            <p>{$t.cookiePolicy?.what.p3}</p>
            <p>{$t.cookiePolicy?.what.p4}</p>
        </section>

        <section>
            <h2>{$t.cookiePolicy?.notCookie.title}</h2>
            <p>{$t.cookiePolicy?.notCookie.p1}</p>
        </section>

        <section>
            <h2>{$t.cookiePolicy?.storedInfo.title}</h2>
            <p>{$t.cookiePolicy?.storedInfo.p1}</p>
            <p>{$t.cookiePolicy?.storedInfo.p2}</p>
            <p>{$t.cookiePolicy?.storedInfo.p3}</p>
        </section>

        <section>
            <h2>{$t.cookiePolicy?.types.title}</h2>
            <p>{$t.cookiePolicy?.types.p1}</p>
            <h3>{$t.cookiePolicy?.types.necessary.title}</h3>
            <p>{$t.cookiePolicy?.types.necessary.p1}</p>
            <p>{$t.cookiePolicy?.types.necessary.p2}</p>
            <p>{$t.cookiePolicy?.types.necessary.p3}</p>
            <h3>{$t.cookiePolicy?.types.preferences.title}</h3>
            <p>{$t.cookiePolicy?.types.preferences.p1}</p>
            <h3>{$t.cookiePolicy?.types.analytics.title}</h3>
            <p>{$t.cookiePolicy?.types.analytics.p1}</p>
            <h3>{$t.cookiePolicy?.types.marketing.title}</h3>
            <p>{$t.cookiePolicy?.types.marketing.p1}</p>
            <h3>{$t.cookiePolicy?.types.geolocation.title}</h3>
            <p>{$t.cookiePolicy?.types.geolocation.p1}</p>
        </section>

        <section>
            <h2>{$t.cookiePolicy?.firstThirdParty.title}</h2>
            <p>{$t.cookiePolicy?.firstThirdParty.p1}</p>
        </section>

        <section>
            <h2>{$t.cookiePolicy?.disabling.title}</h2>
            <p>{$t.cookiePolicy?.disabling.p1}</p>
            <ul>
                {#each $t.cookiePolicy?.disabling.examples || [] as example}
                    <li>{example}</li>
                {/each}
            </ul>
        </section>

        <section>
            <h2>{$t.cookiePolicy?.deletion.title}</h2>
            <p>{$t.cookiePolicy?.deletion.p1}</p>
            <p>{$t.cookiePolicy?.deletion.p2}</p>
        </section>

        <section>
            <h2>{$t.cookiePolicy?.management.title}</h2>
            <p>{$t.cookiePolicy?.management.p1}</p>
            <ul>
                {#each $t.cookiePolicy?.management.browsers || [] as browser}
                    <li><a href={browser.link} target="_blank" rel="noopener noreferrer">{browser.name}</a></li>
                {/each}
            </ul>
        </section>

        <section>
            <h2>{$t.cookiePolicy?.update.title}</h2>
            <p>{$t.cookiePolicy?.update.p1}</p>
        </section>
    </main>

    <Footer />
</div>

<style>
    :global(body) {
        margin: 0;
        padding: 0;
        font-family: 'Montserrat', sans-serif;
        background-color: #000000;
        color: #e3e3e3;
    }

    .app {
        min-height: 100vh;
    }

    .main-content {
        max-width: 800px;
        margin: 0 auto;
        padding: 40px 20px;
    }

    .page-title {
        font-size: 3rem;
        font-weight: 900;
        color: #efc824;
        margin-bottom: 2rem;
        text-align: center;
    }

    section {
        margin-bottom: 2rem;
    }

    h2 {
        font-size: 2rem;
        color: #efc824;
        margin-bottom: 1rem;
    }

    h3 {
        font-size: 1.5rem;
        color: #efc824;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }

    p {
        margin-bottom: 1rem;
        line-height: 1.6;
    }

    ul {
        padding-left: 1.5rem;
        margin-bottom: 1rem;
    }

    li {
        margin-bottom: 0.5rem;
    }

    a {
        color: #efc824;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }
</style>