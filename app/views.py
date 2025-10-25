from flask import render_template, flash, redirect, url_for, request
from .forms import PostForm
from . import app  # Assuming the Flask app instance is imported as 'app'


@app.route('/')
def resume():
    """Renders the resume page."""
    return render_template('resume.html', title="Resume")


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    """Handles the contact page and form validation."""
    form = PostForm()

    # 1. Block executes if the form was submitted (POST) and passed validation
    if form.validate_on_submit():
        try:
            # Gather data from the form
            name = form.name.data
            email = form.email.data
            # phone = form.phone.data  # Unused, but kept for context clarity
            subject = form.subject.data
            message = form.message.data

            # 2. Logging the received data
            log_message = (
                f"CONTACT_FORM: Name={name}, Email={email}, "
                f"Subject={subject}, Message_len={len(message)}"
            )
            app.logger.info(log_message)

            # 3. Flash success message
            flash(
                f"Thank you, {name}! Your message ({email}) has been successfully submitted.",
                "success"
            )

        except Exception as e:
            # 4. Error handling (in case logging or other logic fails)
            app.logger.error(f"Error processing contact form for {email}: {e}")
            flash(
                f"An error occurred while processing your request. Please try again later.",
                "error"
            )
            # Redirect even if an error occurred to prevent resubmission
            return redirect(url_for('contacts'))

        # 5. Post/Redirect/Get pattern: redirect to prevent form resubmission
        return redirect(url_for('contacts'))

    # 6. If it's a POST request but validation failed, flash an error
    if request.method == 'POST':
        flash("Submission error! Please check the highlighted fields.", "error")

    # 7. Render the template (for GET requests or failed POSTs)
    return render_template('contacts.html', title="Contacts", form=form)