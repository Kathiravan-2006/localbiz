// Search functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="search"]');
    const categorySelect = document.querySelector('select[name="category"]');
    const ratingSelect = document.querySelector('select[name="rating"]');
    
    if (searchInput && categorySelect && ratingSelect) {
        const searchForm = document.querySelector('.search-form');
        
        // Debounce function to limit API calls
        function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }
        
        // Handle search input changes
        searchInput.addEventListener('input', debounce(() => {
            searchForm.submit();
        }, 500));
        
        // Handle category and rating changes
        categorySelect.addEventListener('change', () => {
            searchForm.submit();
        });
        
        ratingSelect.addEventListener('change', () => {
            searchForm.submit();
        });
    }
});

// Modal functionality
function showModal(message, callback) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <p>${message}</p>
            <div class="modal-buttons">
                <button class="button confirm">Confirm</button>
                <button class="button cancel">Cancel</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    const confirmBtn = modal.querySelector('.confirm');
    const cancelBtn = modal.querySelector('.cancel');
    
    confirmBtn.addEventListener('click', () => {
        modal.remove();
        if (callback) callback(true);
    });
    
    cancelBtn.addEventListener('click', () => {
        modal.remove();
        if (callback) callback(false);
    });
}

// Delete confirmation
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.button.delete');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const href = button.getAttribute('href');
            
            showModal('Are you sure you want to delete this item?', (confirmed) => {
                if (confirmed) {
                    window.location.href = href;
                }
            });
        });
    });
});

// Star rating functionality
document.addEventListener('DOMContentLoaded', function() {
    const ratingInputs = document.querySelectorAll('input[name="rating"]');
    
    ratingInputs.forEach(input => {
        const stars = input.parentElement.querySelectorAll('.star');
        
        stars.forEach((star, index) => {
            star.addEventListener('mouseover', () => {
                stars.forEach((s, i) => {
                    s.style.color = i <= index ? '#f1c40f' : '#ddd';
                });
            });
            
            star.addEventListener('mouseout', () => {
                stars.forEach((s, i) => {
                    s.style.color = i < input.value ? '#f1c40f' : '#ddd';
                });
            });
            
            star.addEventListener('click', () => {
                input.value = index + 1;
                stars.forEach((s, i) => {
                    s.style.color = i <= index ? '#f1c40f' : '#ddd';
                });
            });
        });
    });
});

// Add modal styles
const style = document.createElement('style');
style.textContent = `
    .modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }
    
    .modal-content {
        background-color: white;
        padding: 2rem;
        border-radius: 5px;
        text-align: center;
    }
    
    .modal-buttons {
        margin-top: 1rem;
        display: flex;
        justify-content: center;
        gap: 1rem;
    }
    
    .star {
        cursor: pointer;
        font-size: 1.5rem;
        color: #ddd;
    }
    
    .star:hover,
    .star.active {
        color: #f1c40f;
    }
`;
document.head.appendChild(style);

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle FAQ accordion
    const faqQuestions = document.querySelectorAll('.faq-question');
    faqQuestions.forEach(question => {
        question.addEventListener('click', () => {
            const answer = question.nextElementSibling;
            answer.style.display = answer.style.display === 'none' ? 'block' : 'none';
            question.classList.toggle('active');
        });
    });

    // Handle business search
    const searchForm = document.querySelector('#search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchInput = this.querySelector('input[name="q"]');
            if (searchInput.value.trim() === '') {
                return;
            }
            this.submit();
        });
    }

    // Handle business filters
    const filterForm = document.querySelector('#filter-form');
    if (filterForm) {
        filterForm.addEventListener('change', function() {
            this.submit();
        });
    }

    // Handle review submission
    const reviewForm = document.querySelector('#review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const rating = this.querySelector('input[name="rating"]:checked');
            const comment = this.querySelector('textarea[name="comment"]');
            
            if (!rating) {
                alert('Please select a rating');
                return;
            }
            
            if (comment.value.trim() === '') {
                alert('Please enter a comment');
                return;
            }
            
            this.submit();
        });
    }

    // Handle business image preview
    const imageInput = document.querySelector('#business-image');
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const preview = document.querySelector('#image-preview');
            const file = this.files[0];
            
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Handle profile image preview
    const profileImageInput = document.querySelector('#profile-image');
    if (profileImageInput) {
        profileImageInput.addEventListener('change', function() {
            const preview = document.querySelector('#profile-preview');
            const file = this.files[0];
            
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Handle contact form validation
    const contactForm = document.querySelector('#contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const name = this.querySelector('input[name="name"]');
            const email = this.querySelector('input[name="email"]');
            const message = this.querySelector('textarea[name="message"]');
            
            if (name.value.trim() === '') {
                alert('Please enter your name');
                return;
            }
            
            if (email.value.trim() === '') {
                alert('Please enter your email');
                return;
            }
            
            if (message.value.trim() === '') {
                alert('Please enter your message');
                return;
            }
            
            this.submit();
        });
    }

    // Handle business status toggle in admin dashboard
    const statusToggles = document.querySelectorAll('.status-toggle');
    statusToggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const businessId = this.dataset.businessId;
            const status = this.checked ? 'active' : 'inactive';
            
            fetch(`/admin/business/${businessId}/status/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ status: status })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('Business status updated successfully', 'success');
                } else {
                    showAlert('Failed to update business status', 'danger');
                    this.checked = !this.checked;
                }
            })
            .catch(error => {
                showAlert('An error occurred while updating business status', 'danger');
                this.checked = !this.checked;
            });
        });
    });

    // Handle user status toggle in admin dashboard
    const userStatusToggles = document.querySelectorAll('.user-status-toggle');
    userStatusToggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const userId = this.dataset.userId;
            const status = this.checked ? 'active' : 'inactive';
            
            fetch(`/admin/user/${userId}/status/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ status: status })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('User status updated successfully', 'success');
                } else {
                    showAlert('Failed to update user status', 'danger');
                    this.checked = !this.checked;
                }
            })
            .catch(error => {
                showAlert('An error occurred while updating user status', 'danger');
                this.checked = !this.checked;
            });
        });
    });
});

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Helper function to show alerts
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
} 