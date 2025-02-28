<script>
    import PublicNavbar from '../common/PublicNavbar.svelte';
    import Footer from '../common/footer.svelte';
    import { t } from '../i18n.js';  // Import the translation store
</script>

<div class="app">
    <PublicNavbar currentPage="landing" />

    <main class="main-content">
        <h1 class="page-title">{$t.privacyPolicy?.title}</h1>

        <section>
            <h2>{$t.privacyPolicy?.scope.title}</h2>
            <p>{$t.privacyPolicy?.scope.p1}</p>
            <p>{$t.privacyPolicy?.scope.p2 }</p>
            <p>{$t.privacyPolicy?.scope.p3 }</p>
        </section>

        <section>
            <h2>{$t.privacyPolicy?.purposes.title }</h2>
            <p>{$t.privacyPolicy?.purposes.p1}</p>
            <p>{$t.privacyPolicy?.purposes.p2 }</p>
            <p>{$t.privacyPolicy?.purposes.p3}</p>
        </section>

        <section>
            <h2>{$t.privacyPolicy?.about.title }</h2>
            <p>{$t.privacyPolicy?.about.p1}</p>
            <p>{$t.privacyPolicy?.about.p2 }</p>
        </section>

        <section>
            <h2>{$t.privacyPolicy?.videoStorage.title }</h2>
            <p>{$t.privacyPolicy?.videoStorage.p1 }</p>
            <p>{$t.privacyPolicy?.videoStorage.p2 }</p>
            <p>{$t.privacyPolicy?.videoStorage.p3 }</p>
            <p>{$t.privacyPolicy?.videoStorage.p4 }</p>
            <p>{$t.privacyPolicy?.videoStorage.p5 }</p>
        </section>

        <section>
            <h2>{$t.privacyPolicy?.confidentiality.title}</h2>
            <p>{$t.privacyPolicy?.confidentiality.p1}</p>
            <p>{$t.privacyPolicy?.confidentiality.p2 }</p>
        </section>

        <section>
            <h2>{$t.privacyPolicy?.rights.title }</h2>
            <p>{$t.privacyPolicy?.rights.p1}</p>
        </section>

        <section>
            <h2>{$t.privacyPolicy?.userRights.title}</h2>
            <p>{$t.privacyPolicy?.userRights.p1}</p>
        </section>

        <section>
            <h2>{$t.privacyPolicy?.salesFunnels.title}</h2>
            <p>{$t.privacyPolicy?.salesFunnels.p1}</p>
        </section>

        <section>
            <h2>{$t.privacyPolicy?.disclaimer.title}</h2>
            <p>{$t.privacyPolicy?.disclaimer.p1}</p>
        </section>

        <section>
            <h2>{$t.privacyPolicy?.modification.title}</h2>
            <p>{$t.privacyPolicy?.modification.p1 }</p>
            <p>{$t.privacyPolicy?.modification.p2 }</p>
            <p>{$t.privacyPolicy?.modification.p3 }</p>
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

    p {
        margin-bottom: 1rem;
        line-height: 1.6;
    }

</style>
