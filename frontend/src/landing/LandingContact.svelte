<script lang="ts">
  import PublicNavbar from '../common/PublicNavbar.svelte';
  import Footer from '../common/footer.svelte';
  import { onMount } from 'svelte';
  import { t } from '../i18n.js';

  // Form values
  let name = '';
  let email = '';
  let role = '';
  let companyName = '';
  let companyWebsite = '';
  let companySize = 'Less than 20 people';
  let annualRevenue = 'Less than €100K/year';
  let projectBudget = '$0 - $5000';
  let services = 'Developing a custom AI solution';
  let helpText = '';
  let preferredLanguage = 'English';
  
  // Form submission status
  let isSubmitting = false;
  let submitError = '';
  let submitSuccess = false;

  // Form submission handling
  async function handleSubmit() {
    isSubmitting = true;
    submitError = '';
    submitSuccess = false;
    
    console.log('Form submission started with data:', {
      name, email, role, companyName, companyWebsite, 
      companySize, annualRevenue, projectBudget, services, helpText, preferredLanguage
    });
    
    try {
      const formData = {
        name, 
        email, 
        role, 
        company_name: companyName, 
        company_website: companyWebsite, 
        company_size: companySize, 
        annual_revenue: annualRevenue, 
        project_budget: projectBudget, 
        services, 
        help_text: helpText, 
        preferred_language: preferredLanguage
      };
      
      console.log('Sending form data to API:', formData);
      
      // Send data to backend API
      const response = await fetch('/api/submit-business-lead/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      console.log('API response status:', response.status, response.statusText);
      const result = await response.json();
      console.log('API response data:', result);
      
      if (!response.ok) {
        throw new Error(result.message || 'An error occurred while submitting the form');
      }
      
      // Show success message and reset form
      console.log('Form submission successful');
      submitSuccess = true;
      resetForm();
    } catch (error: any) {
      console.error('Error submitting form:', error);
      submitError = error.message || $t.features?.aiBusiness?.contact?.errorMessage || 'An error occurred. Please try again.';
    } finally {
      isSubmitting = false;
    }
  }

  function resetForm() {
    name = '';
    email = '';
    role = '';
    companyName = '';
    companyWebsite = '';
    companySize = 'Less than 20 people';
    annualRevenue = 'Less than €100K/year';
    projectBudget = '$0 - $5000';
    services = 'Developing a custom AI solution';
    helpText = '';
    preferredLanguage = 'English';
  }

  let sectionVisible: Record<string, boolean> = {};
  
  onMount(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          sectionVisible[entry.target.id] = true;
        }
      });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('section').forEach(section => {
      observer.observe(section);
    });
  });
</script>

<svelte:head>
  <title>{$t.features?.aiBusiness?.contact?.title || 'Contact Us - AI Automation Solutions | Yekar'}</title>
  <meta name="description" content={$t.features?.aiBusiness?.contact?.description || 'Get in touch to discuss how AI automation can address your specific business challenges.'}>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@900&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
</svelte:head>

<div class="ai-business-contact-page">
  <PublicNavbar currentPage="ai-business-contact" />
  
  <!-- Header Section -->
  <section id="contact-header" class="contact-header-section" class:visible={sectionVisible['contact-header'] || false}>
    <div class="container">
      <h1>{$t.features?.aiBusiness?.contact?.heading || 'Get in Touch'}</h1>
      <p class="subtitle">{$t.features?.aiBusiness?.contact?.subheading || 'Schedule a free consultation to discuss how AI automation can address your specific business challenges'}</p>
    </div>
  </section>
  
  <!-- Contact Form Section -->
  <section id="contact-form" class="contact-form-section" class:visible={sectionVisible['contact-form'] || false}>
    <div class="container">
      <form on:submit|preventDefault={handleSubmit} class="contact-form">
        <div class="form-row">
          <div class="form-group">
            <label for="name">{$t.features?.aiBusiness?.contact?.nameLabel || 'What is your name?'}</label>
            <input type="text" id="name" bind:value={name} placeholder={$t.features?.aiBusiness?.contact?.namePlaceholder || 'Name'} required>
          </div>
          <div class="form-group">
            <label for="email">{$t.features?.aiBusiness?.contact?.emailLabel || 'What is your email?'}</label>
            <input type="email" id="email" bind:value={email} placeholder={$t.features?.aiBusiness?.contact?.emailPlaceholder || 'Email'} required>
          </div>
        </div>
        
        <div class="form-group full-width">
          <label for="role">{$t.features?.aiBusiness?.contact?.roleLabel || 'What is your role within your organization?'}</label>
          <input type="text" id="role" bind:value={role} placeholder={$t.features?.aiBusiness?.contact?.rolePlaceholder || 'Enter role'} required>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="company-name">{$t.features?.aiBusiness?.contact?.companyNameLabel || 'Company name?'}</label>
            <input type="text" id="company-name" bind:value={companyName} placeholder={$t.features?.aiBusiness?.contact?.companyNamePlaceholder || 'Enter company name'}>
          </div>
          <div class="form-group">
            <label for="company-website">{$t.features?.aiBusiness?.contact?.companyWebsiteLabel || 'Company website?'}</label>
            <input type="text" id="company-website" bind:value={companyWebsite} placeholder={$t.features?.aiBusiness?.contact?.companyWebsitePlaceholder || 'Enter company website'}>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="company-size">{$t.features?.aiBusiness?.contact?.companySizeLabel || 'Company size?'}</label>
            <select id="company-size" bind:value={companySize}>
              <option value="Less than 20 people">{$t.features?.aiBusiness?.contact?.companySizeOptions?.option1 || 'Less than 20 people'}</option>
              <option value="20-50 people">{$t.features?.aiBusiness?.contact?.companySizeOptions?.option2 || '20-50 people'}</option>
              <option value="51-200 people">{$t.features?.aiBusiness?.contact?.companySizeOptions?.option3 || '51-200 people'}</option>
              <option value="201-500 people">{$t.features?.aiBusiness?.contact?.companySizeOptions?.option4 || '201-500 people'}</option>
              <option value="501-1000 people">{$t.features?.aiBusiness?.contact?.companySizeOptions?.option5 || '501-1000 people'}</option>
              <option value="1001+ people">{$t.features?.aiBusiness?.contact?.companySizeOptions?.option6 || '1001+ people'}</option>
            </select>
          </div>
          <div class="form-group">
            <label for="preferred-language">{$t.common?.languagePreference?.label || 'What language are you most comfortable in?'}</label>
            <select id="preferred-language" bind:value={preferredLanguage}>
              <option value="English">{$t.common?.languagePreference?.options?.english || 'English'}</option>
              <option value="Spanish">{$t.common?.languagePreference?.options?.spanish || 'Spanish'}</option>
            </select>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="annual-revenue">{$t.features?.aiBusiness?.contact?.revenueLabel || 'Company\'s annual revenue?'}</label>
            <select id="annual-revenue" bind:value={annualRevenue}>
              {#if $t.common?.language === 'es'}
                <option value="Less than $100K/year">{$t.features?.aiBusiness?.contact?.revenueOptions?.option1 || 'Menos de $100K/año'}</option>
                <option value="$100K-$500K/year">{$t.features?.aiBusiness?.contact?.revenueOptions?.option2 || '100K€-500K€/año'}</option>
                <option value="$500K-$1M/year">{$t.features?.aiBusiness?.contact?.revenueOptions?.option3 || '500K€-1M€/año'}</option>
                <option value="$1M-$5M/year">{$t.features?.aiBusiness?.contact?.revenueOptions?.option4 || '1M€-5M€/año'}</option>
                <option value="More than $5M/year">{$t.features?.aiBusiness?.contact?.revenueOptions?.option5 || 'Más de 5M€/año'}</option>
              {:else}
                <option value="Less than $100K/year">{$t.features?.aiBusiness?.contact?.revenueOptions?.option1 || 'Less than $100K/year'}</option>
                <option value="$100K-$500K/year">{$t.features?.aiBusiness?.contact?.revenueOptions?.option2 || '$100K-$500K/year'}</option>
                <option value="$500K-$1M/year">{$t.features?.aiBusiness?.contact?.revenueOptions?.option3 || '$500K-$1M/year'}</option>
                <option value="$1M-$5M/year">{$t.features?.aiBusiness?.contact?.revenueOptions?.option4 || '$1M-$5M/year'}</option>
                <option value="More than $5M/year">{$t.features?.aiBusiness?.contact?.revenueOptions?.option5 || 'More than $5M/year'}</option>
              {/if}
            </select>
          </div>
        </div>
        
        <div class="form-group full-width">
          <label for="project-budget">{$t.features?.aiBusiness?.contact?.budgetLabel || 'Project budget?'}</label>
          <select id="project-budget" bind:value={projectBudget}>
            <option value="$0 - $5000">{$t.features?.aiBusiness?.contact?.budgetOptions?.option1 || '0 - 5000€'}</option>
            <option value="$5000 - $10000">{$t.features?.aiBusiness?.contact?.budgetOptions?.option2 || '5000 - 10000€'}</option>
            <option value="$10000 - $25000">{$t.features?.aiBusiness?.contact?.budgetOptions?.option3 || '10000 - 25000€'}</option>
            <option value="$25000 - $50000">{$t.features?.aiBusiness?.contact?.budgetOptions?.option4 || '25000 - 50000€'}</option>
            <option value="$50000+">{$t.features?.aiBusiness?.contact?.budgetOptions?.option5 || '50000+€'}</option>
          </select>
        </div>
        
        <div class="form-group full-width">
          <label for="services">{$t.features?.aiBusiness?.contact?.servicesLabel || 'What services are you interested in?'}</label>
          <select id="services" bind:value={services}>
            <option value="Developing a custom AI solution">{$t.features?.aiBusiness?.contact?.servicesOptions?.option1 || 'Developing a custom AI solution'}</option>
            <option value="AI integration with existing systems">{$t.features?.aiBusiness?.contact?.servicesOptions?.option2 || 'AI integration with existing systems'}</option>
            <option value="AI strategy consulting">{$t.features?.aiBusiness?.contact?.servicesOptions?.option3 || 'AI strategy consulting'}</option>
            <option value="Data analysis and insights">{$t.features?.aiBusiness?.contact?.servicesOptions?.option4 || 'Data analysis and insights'}</option>
            <option value="AI automation">{$t.features?.aiBusiness?.contact?.servicesOptions?.option5 || 'AI automation'}</option>
            <option value="Other">{$t.features?.aiBusiness?.contact?.servicesOptions?.option6 || 'Other'}</option>
          </select>
        </div>
        
        <div class="form-group full-width">
          <label for="help-text">{$t.features?.aiBusiness?.contact?.messageLabel || 'How can we help?'}</label>
          <textarea id="help-text" bind:value={helpText} placeholder={$t.features?.aiBusiness?.contact?.messagePlaceholder || 'Type your response here...'} rows="5"></textarea>
        </div>
        
        {#if submitError}
          <div class="form-group full-width error-message">
            <p>{submitError}</p>
          </div>
        {/if}
        
        {#if submitSuccess}
          <div class="form-group full-width success-message">
            <p>{$t.features?.aiBusiness?.contact?.successMessage || 'Thank you for your inquiry. We will contact you shortly.'}</p>
          </div>
        {/if}
        
        <div class="form-group submit-group">
          <button type="submit" class="btn btn-primary submit-btn" disabled={isSubmitting}>
            {#if isSubmitting}
              {$t.features?.aiBusiness?.contact?.submittingButton || 'Submitting...'}
            {:else}
              {$t.features?.aiBusiness?.contact?.submitButton || 'Submit'}
            {/if}
          </button>
        </div>
      </form>
    </div>
  </section>
  
  <Footer />
</div>

<style>
  /* General Styles */
  .ai-business-contact-page {
    color: #e3e3e3;
    font-family: 'Roboto', sans-serif;
    background-color: #000000;
  }
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 40px;
  }
  
  section {
    padding: 80px 0;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }
  
  section.visible {
    opacity: 1;
    transform: translateY(0);
  }
  
  h1 {
    margin: 0;
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: 3.5rem;
    line-height: 1.2;
    margin-bottom: 2rem;
    color: #efc824;
  }
  
  .subtitle {
    font-size: 1.25rem;
    color: #e3e3e3;
    margin-bottom: 3rem;
    max-width: 700px;
  }
  
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 16px 32px;
    border-radius: 0;
    font-weight: 600;
    transition: all 0.3s ease;
    text-decoration: none;
    gap: 12px;
    margin-bottom: 12px;
    border: none;
    cursor: pointer;
  }
  
  .btn-primary {
    background-color: #efc824;
    color: #000000;
  }
  
  .btn-primary:hover {
    background-color: #f5d547;
  }
  
  /* Contact Header Section */
  .contact-header-section {
    background-color: #000000;
    padding-top: 120px;
    padding-bottom: 40px;
    text-align: center;
  }
  
  .contact-header-section h1 {
    color: #efc824;
    font-size: 3rem;
    font-weight: 900;
    margin-bottom: 1.5rem;
  }
  
  .contact-header-section p {
    color: #e3e3e3;
    font-size: 1.25rem;
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
    line-height: 1.6;
  }
  
  /* Contact Form Section */
  .contact-form-section {
    background-color: #000000;
    padding-top: 40px;
    padding-bottom: 80px;
  }
  
  .contact-form {
    max-width: 900px;
    margin: 0 auto;
    background-color: #000000;
    padding: 40px;
    border: 1px solid #333;
  }
  
  .form-row {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
  }
  
  .form-group {
    flex: 1;
    display: flex;
    flex-direction: column;
    margin-bottom: 20px;
  }
  
  .full-width {
    width: 100%;
  }
  
  label {
    color: #e3e3e3;
    font-weight: 500;
    margin-bottom: 8px;
    font-size: 1rem;
  }
  
  input, select, textarea {
    padding: 12px 16px;
    background-color: #000000;
    border: 1px solid #333;
    color: #e3e3e3;
    font-family: 'Roboto', sans-serif;
    font-size: 1rem;
    transition: border-color 0.3s ease;
  }
  
  input:focus, select:focus, textarea:focus {
    outline: none;
    border-color: #efc824;
  }
  
  select {
    appearance: none;
    background-image: url("data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23efc824' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 12px center;
    background-size: 16px;
    padding-right: 40px;
  }
  
  .submit-group {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
  }
  
  .submit-btn {
    min-width: 150px;
  }
  
  .error-message {
    background-color: rgba(220, 53, 69, 0.1);
    border: 1px solid rgba(220, 53, 69, 0.5);
    padding: 12px;
    border-radius: 4px;
    color: #dc3545;
    margin-bottom: 20px;
  }
  
  .error-message p {
    margin: 0;
  }
  
  .success-message {
    background-color: rgba(40, 167, 69, 0.1);
    border: 1px solid rgba(40, 167, 69, 0.5);
    padding: 12px;
    border-radius: 4px;
    color: #28a745;
    margin-bottom: 20px;
  }
  
  .success-message p {
    margin: 0;
  }
  
  /* Responsive adjustments */
  @media (max-width: 992px) {
    .form-row {
      flex-direction: column;
      gap: 0;
    }
  }
  
  @media (max-width: 768px) {
    .container {
      padding: 0 24px;
    }
    
    section {
      padding: 60px 0;
    }
    
    h1 {
      font-size: 2.5rem;
    }
    
    .contact-form {
      padding: 24px;
    }
  }
</style> 