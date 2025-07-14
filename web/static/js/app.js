// Custom JavaScript for Automobile Insurance Underwriting System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Loading states for buttons
    const loadingButtons = document.querySelectorAll('.btn[data-loading]');
    loadingButtons.forEach(button => {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            const loadingText = this.getAttribute('data-loading') || 'Loading...';
            
            this.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${loadingText}`;
            this.disabled = true;
            
            // Re-enable after 30 seconds as fallback
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 30000);
        });
    });

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Show success feedback
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check me-2"></i>Copied!';
                this.classList.remove('btn-outline-secondary');
                this.classList.add('btn-success');
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('btn-success');
                    this.classList.add('btn-outline-secondary');
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
                // Show error feedback
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-times me-2"></i>Failed';
                this.classList.add('btn-danger');
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.classList.remove('btn-danger');
                }, 2000);
            });
        });
    });

    // Auto-refresh functionality
    const autoRefreshElements = document.querySelectorAll('[data-auto-refresh]');
    autoRefreshElements.forEach(element => {
        const interval = parseInt(element.getAttribute('data-auto-refresh')) * 1000;
        if (interval > 0) {
            setInterval(() => {
                location.reload();
            }, interval);
        }
    });

    // Progress bar animations
    const progressBars = document.querySelectorAll('.progress-bar[data-animate]');
    progressBars.forEach(bar => {
        const targetWidth = bar.style.width || bar.getAttribute('aria-valuenow') + '%';
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.transition = 'width 1.5s ease-in-out';
            bar.style.width = targetWidth;
        }, 200);
    });

    // Table row highlighting
    const tableRows = document.querySelectorAll('table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(13, 110, 253, 0.1)';
            this.style.transform = 'scale(1.01)';
            this.style.transition = 'all 0.2s ease';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
            this.style.transform = 'scale(1)';
        });
    });

    // Card hover effects
    const hoverCards = document.querySelectorAll('.card[data-hover="true"]');
    hoverCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 1rem 3rem rgba(0, 0, 0, 0.175)';
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
    });

    // Number formatting
    const numberElements = document.querySelectorAll('[data-format="number"]');
    numberElements.forEach(element => {
        const value = parseFloat(element.textContent);
        if (!isNaN(value)) {
            element.textContent = value.toLocaleString();
        }
    });

    // Currency formatting
    const currencyElements = document.querySelectorAll('[data-format="currency"]');
    currencyElements.forEach(element => {
        const value = parseFloat(element.textContent);
        if (!isNaN(value)) {
            element.textContent = new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD'
            }).format(value);
        }
    });

    // Percentage formatting
    const percentageElements = document.querySelectorAll('[data-format="percentage"]');
    percentageElements.forEach(element => {
        const value = parseFloat(element.textContent);
        if (!isNaN(value)) {
            element.textContent = new Intl.NumberFormat('en-US', {
                style: 'percent',
                minimumFractionDigits: 1,
                maximumFractionDigits: 2
            }).format(value / 100);
        }
    });

    // Date formatting
    const dateElements = document.querySelectorAll('[data-format="date"]');
    dateElements.forEach(element => {
        const dateValue = element.textContent;
        const date = new Date(dateValue);
        if (!isNaN(date.getTime())) {
            element.textContent = date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        }
    });

    // Search functionality
    const searchInputs = document.querySelectorAll('[data-search]');
    searchInputs.forEach(input => {
        const targetSelector = input.getAttribute('data-search');
        const targetElements = document.querySelectorAll(targetSelector);
        
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            targetElements.forEach(element => {
                const text = element.textContent.toLowerCase();
                const shouldShow = text.includes(searchTerm);
                
                element.style.display = shouldShow ? '' : 'none';
                
                // Add highlighting
                if (shouldShow && searchTerm) {
                    const regex = new RegExp(`(${searchTerm})`, 'gi');
                    const highlightedText = element.innerHTML.replace(regex, '<mark>$1</mark>');
                    element.innerHTML = highlightedText;
                } else {
                    // Remove existing highlights
                    element.innerHTML = element.textContent;
                }
            });
        });
    });

    // Sortable tables
    const sortableHeaders = document.querySelectorAll('th[data-sort]');
    sortableHeaders.forEach(header => {
        header.style.cursor = 'pointer';
        header.innerHTML += ' <i class="fas fa-sort text-muted"></i>';
        
        header.addEventListener('click', function() {
            const table = this.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            const columnIndex = Array.from(this.parentNode.children).indexOf(this);
            const sortType = this.getAttribute('data-sort');
            
            // Toggle sort direction
            const currentDirection = this.getAttribute('data-direction') || 'asc';
            const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
            this.setAttribute('data-direction', newDirection);
            
            // Update sort icon
            const icon = this.querySelector('i');
            icon.className = `fas fa-sort-${newDirection === 'asc' ? 'up' : 'down'} text-primary`;
            
            // Sort rows
            rows.sort((a, b) => {
                const aValue = a.children[columnIndex].textContent.trim();
                const bValue = b.children[columnIndex].textContent.trim();
                
                let comparison = 0;
                if (sortType === 'number') {
                    comparison = parseFloat(aValue) - parseFloat(bValue);
                } else if (sortType === 'date') {
                    comparison = new Date(aValue) - new Date(bValue);
                } else {
                    comparison = aValue.localeCompare(bValue);
                }
                
                return newDirection === 'asc' ? comparison : -comparison;
            });
            
            // Reorder table rows
            rows.forEach(row => tbody.appendChild(row));
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"], input[data-search]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(modal => {
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) {
                    bsModal.hide();
                }
            });
        }
    });

    // Print functionality
    window.printPage = function() {
        window.print();
    };

    // Export functionality
    window.exportData = function(data, filename, type = 'json') {
        let content, mimeType;
        
        if (type === 'json') {
            content = JSON.stringify(data, null, 2);
            mimeType = 'application/json';
        } else if (type === 'csv') {
            // Convert to CSV
            const headers = Object.keys(data[0] || {});
            const csvContent = [
                headers.join(','),
                ...data.map(row => headers.map(header => `"${row[header] || ''}"`).join(','))
            ].join('\n');
            content = csvContent;
            mimeType = 'text/csv';
        }
        
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    // Theme toggle (if implemented)
    const themeToggle = document.querySelector('[data-theme-toggle]');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
        
        // Load saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            document.documentElement.setAttribute('data-theme', savedTheme);
        }
    }

    // Performance monitoring
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
            }, 0);
        });
    }
});

// Utility functions
window.UW = {
    // Show notification
    notify: function(message, type = 'info', duration = 5000) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }, duration);
    },
    
    // Format numbers
    formatNumber: function(num, decimals = 0) {
        return new Intl.NumberFormat('en-US', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        }).format(num);
    },
    
    // Format currency
    formatCurrency: function(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },
    
    // Format percentage
    formatPercentage: function(value, decimals = 1) {
        return new Intl.NumberFormat('en-US', {
            style: 'percent',
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        }).format(value / 100);
    },
    
    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Throttle function
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

