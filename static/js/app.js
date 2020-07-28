document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary


            //  Step 1 - categories

            let categories = document.querySelectorAll('.step1 .form-group--checkbox');
            const categories_ids = [];
            const categories_names = [];
            for (let el of categories) {
                if (el.children[0].children[0].checked === true) {
                    categories_ids.push(parseInt(el.children[0].children[0].value));
                    categories_names.push(el.children[0].children[2].textContent);
                }
            }
            console.log(categories);
            console.log(categories_ids);
            console.log(categories_names);

            //  Step 2 - number of donated bags
            let bags = document.querySelector('.step2 .form-group--inline');
            let no_of_bags = parseInt(bags.children[0].children[0].value);
            console.log(bags);
            console.log(no_of_bags);


            //  Step 3 - institutions
            let institutions = document.querySelectorAll('.step3 .form-group--checkbox');
            const institution_id = [];
            const institution_name = [];
            for (let el of institutions) {
                if (el.children[0].children[0].checked === true) {
                    institution_id.push(parseInt(el.children[0].children[0].value));
                    institution_name.push(el.children[0].children[2].children[0].textContent);
                }
            }
            console.log(institutions);
            console.log(institution_id);
            console.log(institution_name);

            if (this.currentStep == 3) {
                let institutions_categories = document.querySelectorAll('.step3 .form-group--checkbox #categories');
                console.log(institutions_categories)
                institutions_categories.forEach(institution_category => {
                    institution_category.parentElement.style.display = 'none';
                    let institutions_categories_ids = [];
                    institution_category.value.toString().split(',').forEach(el => {
                        let value = parseInt(el, 10);
                        if (!isNaN(value)) {
                            institutions_categories_ids.push(value);
                        }
                    });
                    let bool = true;
                    categories_ids.forEach(id => {
                        if (!institutions_categories_ids.includes(id)) {
                            bool = false;
                        }
                    });
                    if (bool) {
                        institution_category.parentElement.style.display = 'block';
                    }
                });
            }


            //  Step 4 - information of pick up the item by the courier

            const address = {};
            const donation_reception = {};


            let street = document.querySelector('#address');
            address['street'] = street.value;

            let city = document.querySelector('#city');
            address['city'] = city.value;

            let postcode = document.querySelector('#postcode');
            address['postcode'] = postcode.value;

            let phone = document.querySelector('#phone');
            address['phone'] = phone.value;

            let date = document.querySelector('#date');
            donation_reception['date'] = date.value;

            let time = document.querySelector('#time');
            donation_reception['time'] = time.value;

            let more_info = document.querySelector('#more_info');
            donation_reception['more_info'] = more_info.value;

            console.log(address);
            console.log(donation_reception);

            //  Step 5 - summary

            let bag = document.querySelector('.bag');
            bag.textContent = no_of_bags;

            let category = document.querySelector('.categories');
            category.textContent = categories_names;

            let organization = document.querySelector('.organization');
            organization.textContent = institution_name;

            const addressinfo = document.querySelector('.address');
            addressinfo.children[1].children[0].innerHTML = address['street'];
            addressinfo.children[1].children[1].innerHTML = address['city'];
            addressinfo.children[1].children[2].innerHTML = address['postcode'];
            addressinfo.children[1].children[3].innerHTML = address['phone'];
            const dateinfo = document.querySelector('.date');
            dateinfo.children[1].children[0].innerHTML = donation_reception['date'];
            dateinfo.children[1].children[1].innerHTML = donation_reception['time'];
            dateinfo.children[1].children[2].innerHTML = donation_reception['more_info'];

            var formedObject = new Object();
            formedObject.categories_ids = categories_ids;
            formedObject.no_of_bags = no_of_bags;
            formedObject.institution_id = institution_id;
            formedObject.address = address;
            formedObject.donation_reception = donation_reception;

            var stringFormedObject = JSON.stringify(formedObject)
            this.stringFormedObj = stringFormedObject

            console.log(formedObject);
            console.log(stringFormedObject);
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {    // catch the form's submit event
            e.preventDefault();
            var el = document.getElementsByName("csrfmiddlewaretoken");
            var csrf_value = el[0].getAttribute("value");
            console.log('csrf: ' + csrf_value);
            this.currentStep++;
            this.updateForm();


            $.ajax({    // create an AJAX call...
                type: 'POST',
                url: '/adddonation/',
                data: {
                    'add_donation': this.stringFormedObj,
                    csrfmiddlewaretoken: csrf_value
                },
                success: function () {
                    window.location.assign("/donationconfirm/");
                },
                error: function(data) {
                    alert("Błędne lub niekompletne dane");
                    window.location.reload();

                 }
            });
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});
