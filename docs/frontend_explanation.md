Frontend Architecture Explanation:

1. Source Code Organization:
   - Main source code location: /frontend/src/
   - Technology stack: Svelte framework for component-based UI development
   - Build configuration: /frontend/rollup.config.js (compiles Svelte to static JS)

2. Static Asset Management:
   - Output directory: /frontend/static/
   - Serving mechanism: Django static file serving
   
3. Template Structure:
   - Template directory: /frontend/templates/
   - Naming convention: Example - /frontend/templates/app.html
   - Integration: Templates consume static assets from /frontend/static/

4. Django Integration:
   - Frontend app name: /backend/front
   - Key files:
     * URL routing: /backend/front/urls.py
     * View controllers: /backend/front/views.py

Note: This architecture follows a hybrid approach where Django serves as the backend framework while Svelte handles the frontend interactivity through compiled JavaScript.

The command to update the frontend is "python update_front.py" in the main directory.
