# INGLAT - Renewable Energy Solutions Platform

**Transforming Argentina's energy landscape through intelligent solar installations and advanced monitoring systems.**

INGLAT is a comprehensive web platform for renewable energy installations and management, specializing in photovoltaic systems. Our mission is to make solar energy accessible, profitable, and easy to understand for businesses and individuals across Argentina and Spain

## What Makes INGLAT Special

**Smart Solar Calculator**: Our advanced simulator considers Argentina-specific factors including provincial irradiation levels, roof orientation, installation costs, and even electric vehicle integration. Get accurate ROI calculations tailored to your exact location and needs.

**Proven Portfolio**: Browse our extensive gallery of completed solar installations across Argentina, from residential rooftops to industrial-scale projects. Each case study includes technical specifications, performance data, and real client testimonials.

**Instant WhatsApp Connect**: Smart device detection automatically opens WhatsApp app on mobile or WhatsApp Web on desktop, making consultation requests seamless and immediate.

**Provincial Expertise**: Comprehensive database covering all 24 Argentine provinces and part of Spain with location-specific solar irradiation data, regulatory information, and cost optimization.

## Key Features

### Solar Energy Simulator
- **Comprehensive Calculations**: Power sizing, installation costs, battery systems, and payback analysis
- **Argentina-Focused**: Province-specific irradiation data and local cost structures
- **Future-Ready**: Electric vehicle integration planning
- **Multiple Scenarios**: Compare options with and without battery storage systems

### Project Portfolio Management  
- **Dynamic Showcase**: Admin-managed gallery of completed installations
- **Technical Details**: Power capacity, client type, completion dates, and performance metrics
- **SEO Optimized**: Structured data and metadata for better search visibility
- **Mobile Responsive**: Beautiful presentation across all devices

### Professional Contact System
- **Multi-Channel Approach**: Contact forms, WhatsApp integration, and direct call options
- **Smart Device Detection**: Automatic WhatsApp app/web routing based on device type
- **Lead Management**: Organized inquiry handling through Django admin

### Content Management
- **News & Insights**: Blog system for renewable energy news and company updates
- **Expert Content**: Technical guides and industry analysis
- **SEO Excellence**: Optimized for search engines with proper schema markup

## Technology Stack

**Backend**: Django 5.2.4 with Python 3.11+ for robust, scalable performance
**Database**: PostgreSQL for reliable data management and complex queries
**Frontend**: Modern HTML5, CSS3, and vanilla JavaScript for fast loading times
**Integration**: Smart WhatsApp connectivity with fallback options
**Architecture**: Clean separation of concerns with dedicated Django apps

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Virtual environment (recommended)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd codigo

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements/development.txt

# Environment setup
cp .env.example .env  # Configure your database and secret key

# Database setup
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to see INGLAT in action.

## Project Architecture

### Django Applications
- **Core**: Homepage, about us, services, and main project models
- **Projects**: Portfolio management and showcase functionality  
- **Contact**: Multi-channel contact system with WhatsApp integration
- **Blog**: News and educational content management
- **Dashboard**: Future client monitoring capabilities (planned)

### Database Models
The solar simulator uses sophisticated models for accurate calculations:
- **SimuladorConfig**: Global calculation parameters
- **CostoInstalacion**: Installation costs by power ranges
- **FactorUbicacion**: Solar irradiation by Argentine provinces  
- **FactorOrientacion**: Efficiency factors by roof orientation
- **TipoTejado**: Roof complexity and installation factors
- **AnguloTejado**: Inclination optimization data

## Development Philosophy

**Argentina First**: Every calculation, cost estimate, and feature is optimized for the Argentine renewable energy market.

**Performance Matters**: Fast page loads, optimized images, and efficient database queries ensure excellent user experience across all devices.

**Professional Standards**: Clean code, comprehensive documentation, and proper testing practices maintain enterprise-level quality.

**Future Ready**: Modular architecture supports planned dashboard features for client monitoring and advanced analytics.

## Contributing

INGLAT welcomes contributions from developers passionate about renewable energy and sustainable technology. Our development workflow emphasizes:

- **Documentation First**: Comprehensive guides in `/docs/` directory
- **Code Quality**: PEP 8 compliance and meaningful variable names in Spanish for team collaboration
- **Testing**: Django's built-in testing framework with plans for pytest-django integration
- **Security**: Environment variables for sensitive settings and proper input validation

### Getting Started with Development
1. Review `/docs/PRD.md` for product requirements and business context
2. Check `/docs/UI_UX_doc.md` for design guidelines and color schemes  
3. Consult `/docs/Bug_tracking.md` for known issues and solutions
4. Follow CSS/JS conventions: separate files in `/static/` with proper Django template integration

## Business Impact

INGLAT represents more than just a website—it's a platform for accelerating Argentina's transition to renewable energy. By making solar calculations accessible and accurate, we're helping businesses and individuals make informed decisions about sustainable energy investments.

Our focus on the Argentine market means every feature, calculation, and design decision considers local regulations, climate conditions, and economic factors. This local expertise, combined with modern web technology, creates a powerful tool for renewable energy adoption.

## Contact

Ready to explore renewable energy solutions for your business or home?

**Company**: INGLAT - Renewable Energy Solutions  
**Website**: [Coming Soon - Professional Domain]  
**WhatsApp**: +54 11 6721-4369  
**Focus Area**: Argentina (All Provinces)

---

**Built with Django 5.2.4 | Designed for Argentina's Renewable Energy Future**