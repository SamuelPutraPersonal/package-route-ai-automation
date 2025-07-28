# PackageRouteAI Test Automation Suite

This project demonstrates automated API testing for a simulated package recognition and routing system (PackageRouteAI), inspired by Prime Vision's domain. It utilizes Python, Pytest, Requests, and Allure for comprehensive test reporting, integrated with GitHub Actions for CI/CD.

## Project Structure
package_route_ai_automation/
├── .github/                 # GitHub Actions CI/CD workflows (will be added later)
├── src/                     # Source code for the test framework
│   └── api/                 # API interaction layer (PackageRouteAPI client)
├── tests/                   # Test cases
│   └── api/                 # API tests
├── test_data/               # Sample data for tests (e.g., images)
├── reports/                 # Generated test reports (ignored by Git)
├── requirements.txt         # Python dependencies
├── .env.example             # Example environment variables
├── .gitignore               # Files/folders to ignore in Git
└── README.md                # This documentation


## System Under Test (SUT)

This automation suite tests a hypothetical Flask API application called `PackageRouteAI`.
**Important:** The `PackageRouteAI` application itself is assumed to be running at `http://127.0.0.1:5000`. You can find its source code in a sibling directory: `../package_route_ai_sut`.

## Technologies Used

* **Python:** Programming language for tests.
* **Pytest:** Test framework for structuring and running tests.
* **Requests:** HTTP library for API interactions.
* **Allure Report:** For rich, interactive test reporting.
* **GitHub Actions:** For Continuous Integration and Continuous Delivery (to be configured).

## Setup Instructions

1.  **Clone this repository:**
    ```bash
    git clone [https://github.com/your-username/package-route-ai-automation.git](https://github.com/your-username/package-route-ai-automation.git)
    cd package_route_ai_automation
    ```
2.  **Create a Python Virtual Environment (recommended):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows: `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Install Allure Command Line Tool:**
    (Refer to Allure's official documentation for installation on your OS if not already installed. E.g., `choco install allure` on Windows or manual install.)
    (Requires Java 8 or higher: install OpenJDK if needed)
5.  **Configure Environment Variables:**
    Create a `.env` file in the root of the project based on `.env.example`:
    ```bash
    copy .env.example .env
    ```
    Ensure `PRIME_VISION_SUT_API_BASE_URL` points to your running SUT (default is `http://127.0.0.1:5000`).

## How to Run Tests Locally

1.  **Ensure `PackageRouteAI` SUT is running:**
    Open a separate Anaconda Prompt and navigate to your `package_route_ai_sut` directory.
    ```bash
    cd C:\Users\YourWindowsUsername\Desktop\prime_vision_projects\package_route_ai_sut # Adjust path
    python app.py
    ```
    (Keep this terminal open while running tests)
2.  **Activate virtual environment (if not already):**
    From the `package_route_ai_automation` directory in its own Anaconda Prompt:
    ```bash
    .\venv\Scripts\activate
    ```
3.  **Run Pytest tests and generate Allure results:**
    ```bash
    pytest --alluredir=reports/allure-results
    ```
    This will create raw Allure data in the `reports/allure-results` directory.

## Viewing Test Reports (Allure)

1.  **Ensure Allure Command Line Tool is installed.**
2.  **Serve the report:**
    From the `package_route_ai_automation` directory:
    ```bash
    allure serve reports/allure-results
    ```
    This will process the raw data and open an interactive HTML report in your default web browser.

## CI/CD with GitHub Actions

This project is configured with a GitHub Actions workflow (`.github/workflows/main.yml`) that automatically runs tests on every push and pull request to the `main` branch. It also generates and publishes the Allure Report to GitHub Pages.

* **Workflow:** `.github/workflows/main.yml` (to be created)
* **Live Reports:** [Link to your GitHub Pages Allure Report - will be available after setting up GitHub Actions and pushing]

---
*Developed by [Your Name]*

