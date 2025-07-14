# Automobile Insurance Underwriting System

##  **Complete AI-Powered Underwriting Platform**

A comprehensive automobile insurance underwriting system featuring:
- **AI-Powered Decision Making** with OpenAI GPT-4 integration
- **Advanced A/B Testing Framework** for business optimization
- **Modern Web Interface** with Flask frontend
- **Professional CLI Tools** for automation and testing
- **Comprehensive Rule Engine** with configurable policies

## ISSUES NEEDING RESOLUTION/FIXING

### Functionality
1. HIGH PRIORITY - Need to be able to load and launch this on Streamlit Community App deployment.   Current deployment throws errors while trying to install the dependecies.  Not sure if the error is coming from the pyproject.toml or the requirement.txt file

2. Evaluate.py
   Line 146:  If the user selects from line 128, then it should populate all the fields in Evaluate.py with the user selected data



##  **Quick Start**

### **Web Interface (Recommended)**
```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
# Edit .env and add your OPENAI_API_KEY

# Start web server
python main.py web --debug

# Open browser to http://127.0.0.1:5000
```

### **Command Line Interface**
```bash
# Basic underwriting test
python main.py basic --test

# A/B testing comparison
python main.py ab-test --rule-comparison standard liberal

# Interactive evaluation
python main.py basic --interactive
```

##  **Web Interface Features**

### **Modern, Professional Design**
- **Responsive Bootstrap 5** interface
- **Interactive forms** with real-time validation
- **Visual result displays** with charts and indicators
- **Mobile-optimized** for all devices
- **Professional styling** with animations and hover effects

### **Core Web Functionality**
- ** Applicant Evaluation**: Comprehensive form-based evaluation
- ** Quick Testing**: Pre-configured sample applicants
- ** A/B Testing Dashboard**: Statistical comparison interface
- * Configuration Management**: Rule and policy settings
- ** Documentation**: Built-in help and guides

### **User Experience**
- **Smart Form Validation**: Real-time feedback and suggestions
- **Visual Risk Indicators**: Color-coded credit scores and risk factors
- **Detailed Results**: Comprehensive evaluation breakdowns
- **Export Options**: Print and copy functionality
- **Error Handling**: Professional error pages and messaging

##  **System Architecture**

### **Project Structure**
```
automobile-underwriting-system/
├── main.py                          #  Main entry point
├── pyproject.toml                   # Modern Python config
├── requirements.txt                 # Dependencies
├── .env.example                     # Environment template
│
├── underwriting/                    #  Main package
│   ├── core/                        # Business logic
│   │   ├── models.py               # Pydantic data models
│   │   ├── engine.py               # LLM underwriting engine
│   │   └── exceptions.py           # Custom exceptions
│   ├── ai/                         # AI components
│   │   └── prompts.py              # LangChain prompt templates
│   ├── testing/                    # A/B testing framework
│   │   ├── ab_engine.py            # Comparison engine
│   │   └── statistical_analysis.py # Statistical testing
│   ├── web/                        #  Flask web interface
│   │   ├── app.py                  # Flask application
│   │   ├── routes.py               # Web routes
│   │   ├── forms.py                # Web forms
│   │   ├── templates/              # HTML templates
│   │   └── static/                 # CSS, JS, assets
│   ├── cli/                        # Command-line interfaces
│   ├── data/                       # Sample data and generators
│   └── utils/                      # Utilities and helpers
│
├── config/rules/                   #  Underwriting rules
│   ├── underwriting_rules.json    # Standard rules
│   ├── underwriting_rules_conservative.json
│   └── underwriting_rules_liberal.json
│
├── tests/                          #  Test suite
└── docs/                           #  Documentation
```

##  **AI-Powered Features**

### **LangChain + OpenAI Integration**
- **GPT-4 Analysis**: Intelligent risk assessment
- **Prompt Engineering**: Optimized decision-making prompts
- **Configurable Rules**: JSON-based business rule engine
- **Multiple Strategies**: Conservative, Standard, Liberal approaches

### **Decision Types**
- ** ACCEPT**: Approved for coverage
- ** DENY**: Application rejected
- ** ADJUDICATE**: Manual review required

### **Risk Assessment**
- **Credit Score Analysis**: 300-850 range evaluation
- **Driving History**: Violations and claims analysis
- **Coverage History**: Lapse detection and impact
- **Vehicle Assessment**: Type and value considerations

##  **A/B Testing Framework**

### **Testing Capabilities**
- **Rule Comparison**: Conservative vs Liberal policies
- **Prompt Testing**: Different AI instruction approaches
- **Statistical Analysis**: Chi-square, t-tests, confidence intervals
- **Business Impact**: Loss ratio and ROI calculations

### **Available Comparisons**
```bash
# Compare rule configurations
python main.py ab-test --rule-comparison standard conservative

# Compare prompt approaches
python main.py ab-test --prompt-comparison balanced detailed

# Comprehensive analysis
python main.py ab-test --comprehensive --export results.json
```

##  **Configuration Options**

### **Underwriting Rules**
- **Standard**: Balanced risk approach
- **Conservative**: Stricter acceptance criteria
- **Liberal**: More lenient evaluation

### **Prompt Templates**
- **Balanced**: Standard evaluation approach
- **Conservative**: Risk-averse decision making
- **Liberal**: Growth-oriented evaluation
- **Detailed**: Comprehensive analysis
- **Concise**: Quick decision making

##  **Business Impact Analysis**

### **Key Metrics**
- **Acceptance Rates**: Policy approval percentages
- **Loss Ratio Impact**: Risk assessment accuracy
- **Processing Efficiency**: Automation vs manual review
- **Market Share**: Competitive positioning analysis

### **Statistical Testing**
- **Significance Testing**: 95% confidence intervals
- **Effect Size Calculation**: Cohen's d, Cramér's V
- **Business Recommendations**: Data-driven insights
- **Performance Monitoring**: Continuous optimization

##  **Security & Production**

### **Security Features**
- **CSRF Protection**: Form security tokens
- **Input Validation**: Pydantic model validation
- **Error Handling**: Secure error messaging
- **Environment Variables**: Secure configuration

### **Production Deployment**
```bash
# Production web server
python main.py web --host 0.0.0.0 --port 8080

# Or use with WSGI server
gunicorn "underwriting.web.app:create_app()" --bind 0.0.0.0:8080
```

##  **Documentation**

- **`WEB_FRONTEND_GUIDE.md`**: Complete web interface documentation
- **`AB_TESTING_GUIDE.md`**: A/B testing framework guide
- **`PROJECT_SUMMARY.md`**: Technical architecture overview
- **Built-in Help**: Web interface documentation pages

##  **Use Cases**

### **Insurance Companies**
- **Automated Underwriting**: Reduce manual processing time
- **Risk Optimization**: Data-driven policy adjustments
- **A/B Testing**: Optimize business rules for profitability
- **Compliance**: Consistent, auditable decision making

### **Development Teams**
- **AI Integration**: LangChain and OpenAI implementation example
- **Web Development**: Modern Flask application architecture
- **Testing Framework**: Statistical A/B testing implementation
- **Python Best Practices**: Professional project structure

##  **Getting Started**

1. **Clone and Setup**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Configure environment
   cp .env.example .env
   # Add your OPENAI_API_KEY to .env
   ```

2. **Choose Your Interface**
   ```bash
   # Web interface (recommended)
   python main.py web --debug
   
   # Command line
   python main.py basic --test
   ```

3. **Explore Features**
   - Evaluate sample applicants
   - Test different rule configurations
   - Run A/B testing comparisons
   - Review statistical analysis

##  **Ready for Production**

This system provides a complete foundation for:
- **Enterprise underwriting automation**
- **AI-powered decision making**
- **Data-driven business optimization**
- **Modern web application development**
- **Statistical testing and analysis**

**Start exploring the future of insurance underwriting today!**

