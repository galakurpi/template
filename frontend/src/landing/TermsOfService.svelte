<script>
    import PublicNavbar from '../common/PublicNavbar.svelte';
    import Footer from '../common/footer.svelte';
    import { t } from '../i18n.js';
</script>

<div class="app">
    <PublicNavbar currentPage="landing" />

        <h1 class="page-title">{$t.termsOfService?.title}</h1>

        <section>
            <h2>{$t.termsOfService?.acceptance.title}</h2>
            <p>{$t.termsOfService?.acceptance.p1}</p>
        </section>

        <section>
            <h2>{$t.termsOfService?.description.title}</h2>
            <p>{$t.termsOfService?.description.p1}</p>
        </section>

        <section>
            <h2>{$t.termsOfService?.userObligations.title}</h2>
            <p>{$t.termsOfService?.userObligations.p1}</p>
        </section>

        <section>
            <h2>{$t.termsOfService?.intellectualProperty.title}</h2>
            <p>{$t.termsOfService?.intellectualProperty.p1}</p>
        </section>

        <section>
            <h2>{$t.termsOfService?.limitation.title}</h2>
            <p>{$t.termsOfService?.limitation.p1}</p>
        </section>

        <section>
            <h2>{$t.termsOfService?.termination.title}</h2>
            <p>{$t.termsOfService?.termination.p1}</p>
        </section>

        <section>
            <h2>{$t.termsOfService?.changes.title}</h2>
            <p>{$t.termsOfService?.changes.p1}</p>
        </section>

        <section>
            <h2>{$t.termsOfService?.governing.title}</h2>
            <p>{$t.termsOfService?.governing.p1}</p>
        </section>

        <section>
            <h2>{$t.termsOfService?.contact.title}</h2>
            <p>{$t.termsOfService?.contact.p1}</p>
        </section>

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

    p {
        margin-bottom: 1rem;
        line-height: 1.6;
    }

    a {
        color: #efc824;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }
</style>

