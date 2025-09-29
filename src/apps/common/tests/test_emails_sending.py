from unittest.mock import Mock, patch

from django.conf import settings
from django.template import TemplateDoesNotExist
from django.test import SimpleTestCase, override_settings

from apps.common.services.emails_sending import send_email


class SendEmailTestCase(SimpleTestCase):
    """Test cases for the send_email function."""

    def setUp(self):
        """Set up test data."""
        self.template_name = "welcome"
        self.recipients = ["test@example.com"]
        self.context = {"user_name": "John Doe"}
        self.from_email = "sender@example.com"

    @patch("apps.common.services.emails_sending.render_to_string")
    @patch("apps.common.services.emails_sending.EmailMultiAlternatives")
    def test_send_email_success(self, mock_email_class, mock_render):
        """Test successful email sending with all parameters."""
        # Arrange
        mock_render.side_effect = [
            "Welcome to our platform",  # subject
            "Welcome John Doe!",  # text content
            "<h1>Welcome John Doe!</h1>",  # html content
        ]
        mock_email_instance = Mock()
        mock_email_class.return_value = mock_email_instance

        # Act
        send_email(
            template_name=self.template_name,
            recipients=self.recipients,
            context=self.context,
            from_email=self.from_email,
        )

        # Assert
        # Check that render_to_string was called correctly
        expected_context = {
            **self.context,
            "site_url": settings.SITE_URL,
            "project_name": settings.PROJECT_NAME,
        }
        mock_render.assert_any_call(
            "emails/welcome/subject.txt", context=expected_context
        )
        mock_render.assert_any_call(
            "emails/welcome/body.txt", context=expected_context
        )
        mock_render.assert_any_call(
            "emails/welcome/body.html", context=expected_context
        )

        # Check that EmailMultiAlternatives was created correctly
        mock_email_class.assert_called_once_with(
            subject="Welcome to our platform",
            body="Welcome John Doe!",
            from_email=self.from_email,
            to=self.recipients,
        )

        # Check that HTML alternative was attached
        mock_email_instance.attach_alternative.assert_called_once_with(
            "<h1>Welcome John Doe!</h1>", "text/html"
        )

        # Check that email was sent
        mock_email_instance.send.assert_called_once()

    @patch("apps.common.services.emails_sending.render_to_string")
    @patch("apps.common.services.emails_sending.EmailMultiAlternatives")
    def test_send_email_with_string_recipient(
        self, mock_email_class, mock_render
    ):
        """Test email sending with single string recipient."""
        # Arrange
        mock_render.side_effect = [
            "Subject",
            "Text content",
            "HTML content",
        ]
        mock_email_instance = Mock()
        mock_email_class.return_value = mock_email_instance

        # Act
        send_email(
            template_name=self.template_name,
            recipients="single@example.com",  # Single string instead of list
            context=self.context,
        )

        # Assert
        mock_email_class.assert_called_once()
        call_args = mock_email_class.call_args
        self.assertEqual(call_args[1]["to"], ["single@example.com"])

    @patch("apps.common.services.emails_sending.render_to_string")
    @patch("apps.common.services.emails_sending.EmailMultiAlternatives")
    def test_send_email_with_none_context(self, mock_email_class, mock_render):
        """Test email sending with None context."""
        # Arrange
        mock_render.side_effect = [
            "Subject",
            "Text content",
            "HTML content",
        ]
        mock_email_instance = Mock()
        mock_email_class.return_value = mock_email_instance

        # Act
        send_email(
            template_name=self.template_name,
            recipients=self.recipients,
            context=None,  # None context
        )

        # Assert
        expected_context = {
            "site_url": settings.SITE_URL,
            "project_name": settings.PROJECT_NAME,
        }
        mock_render.assert_any_call(
            "emails/welcome/subject.txt", context=expected_context
        )

    @patch("apps.common.services.emails_sending.render_to_string")
    @patch("apps.common.services.emails_sending.EmailMultiAlternatives")
    @override_settings(DEFAULT_FROM_EMAIL="default@example.com")
    def test_send_email_with_default_from_email(
        self, mock_email_class, mock_render
    ):
        """
        Test email sending uses DEFAULT_FROM_EMAIL when from_email is None.
        """
        # Arrange
        mock_render.side_effect = [
            "Subject",
            "Text content",
            "HTML content",
        ]
        mock_email_instance = Mock()
        mock_email_class.return_value = mock_email_instance

        # Act
        send_email(
            template_name=self.template_name,
            recipients=self.recipients,
            context=self.context,
            from_email=None,  # Should use DEFAULT_FROM_EMAIL
        )

        # Assert
        mock_email_class.assert_called_once()
        call_args = mock_email_class.call_args
        self.assertEqual(call_args[1]["from_email"], "default@example.com")

    @patch("apps.common.services.emails_sending.render_to_string")
    @patch("apps.common.services.emails_sending.EmailMultiAlternatives")
    def test_send_email_context_extension(self, mock_email_class, mock_render):
        """Test that context is properly extended with built-in variables."""
        # Arrange
        mock_render.side_effect = [
            "Subject",
            "Text content",
            "HTML content",
        ]
        mock_email_instance = Mock()
        mock_email_class.return_value = mock_email_instance

        custom_context = {"custom_var": "custom_value"}

        # Act
        send_email(
            template_name=self.template_name,
            recipients=self.recipients,
            context=custom_context,
        )

        # Assert
        expected_context = {
            "custom_var": "custom_value",
            "site_url": settings.SITE_URL,
            "project_name": settings.PROJECT_NAME,
        }

        # Check that all render calls received the extended context
        for call in mock_render.call_args_list:
            self.assertEqual(call[1]["context"], expected_context)

    @patch("apps.common.services.emails_sending.render_to_string")
    def test_send_email_template_not_found(self, mock_render):
        """Test handling of missing template files."""
        # Arrange
        mock_render.side_effect = TemplateDoesNotExist("Template not found")

        # Act & Assert
        with self.assertRaises(TemplateDoesNotExist):
            send_email(
                template_name="nonexistent",
                recipients=self.recipients,
                context=self.context,
            )

    @patch("apps.common.services.emails_sending.render_to_string")
    @patch("apps.common.services.emails_sending.EmailMultiAlternatives")
    def test_send_email_multiple_recipients(
        self, mock_email_class, mock_render
    ):
        """Test email sending to multiple recipients."""
        # Arrange
        mock_render.side_effect = [
            "Subject",
            "Text content",
            "HTML content",
        ]
        mock_email_instance = Mock()
        mock_email_class.return_value = mock_email_instance

        multiple_recipients = [
            "user1@example.com",
            "user2@example.com",
            "user3@example.com",
        ]

        # Act
        send_email(
            template_name=self.template_name,
            recipients=multiple_recipients,
            context=self.context,
        )

        # Assert
        mock_email_class.assert_called_once()
        call_args = mock_email_class.call_args
        self.assertEqual(call_args[1]["to"], multiple_recipients)

    @patch("apps.common.services.emails_sending.render_to_string")
    @patch("apps.common.services.emails_sending.EmailMultiAlternatives")
    def test_send_email_subject_stripped(self, mock_email_class, mock_render):
        """Test that subject is properly stripped of whitespace."""
        # Arrange
        mock_render.side_effect = [
            "  Subject with whitespace  \n",  # subject with whitespace
            "Text content",
            "HTML content",
        ]
        mock_email_instance = Mock()
        mock_email_class.return_value = mock_email_instance

        # Act
        send_email(
            template_name=self.template_name,
            recipients=self.recipients,
            context=self.context,
        )

        # Assert
        mock_email_class.assert_called_once()
        call_args = mock_email_class.call_args
        self.assertEqual(call_args[1]["subject"], "Subject with whitespace")

    @patch("apps.common.services.emails_sending.render_to_string")
    @patch("apps.common.services.emails_sending.EmailMultiAlternatives")
    def test_send_email_template_paths(self, mock_email_class, mock_render):
        """Test that correct template paths are used."""
        # Arrange
        mock_render.side_effect = [
            "Subject",
            "Text content",
            "HTML content",
        ]
        mock_email_instance = Mock()
        mock_email_class.return_value = mock_email_instance

        template_name = "password_reset"

        # Act
        send_email(
            template_name=template_name,
            recipients=self.recipients,
            context=self.context,
        )

        # Assert
        expected_calls = [
            (
                ("emails/password_reset/subject.txt",),
                {"context": mock_render.call_args_list[0][1]["context"]},
            ),
            (
                ("emails/password_reset/body.txt",),
                {"context": mock_render.call_args_list[1][1]["context"]},
            ),
            (
                ("emails/password_reset/body.html",),
                {"context": mock_render.call_args_list[2][1]["context"]},
            ),
        ]

        actual_calls = [
            ((call[0][0],), {"context": call[1]["context"]})
            for call in mock_render.call_args_list
        ]

        self.assertEqual(actual_calls, expected_calls)

    @patch("apps.common.services.emails_sending.render_to_string")
    @patch("apps.common.services.emails_sending.EmailMultiAlternatives")
    def test_send_email_logging_on_exception(
        self, mock_email_class, mock_render
    ):
        """Test that exceptions during email sending are properly handled."""
        # Arrange
        mock_render.side_effect = [
            "Subject",
            "Text content",
            "HTML content",
        ]
        mock_email_instance = Mock()
        mock_email_instance.send.side_effect = Exception("SMTP Error")
        mock_email_class.return_value = mock_email_instance

        # Act & Assert
        with self.assertRaises(Exception):
            send_email(
                template_name=self.template_name,
                recipients=self.recipients,
                context=self.context,
            )

    @patch("apps.common.services.emails_sending.render_to_string")
    @patch("apps.common.services.emails_sending.EmailMultiAlternatives")
    @override_settings(
        SITE_URL="https://testdomain.com", PROJECT_NAME="Test Project"
    )
    def test_send_email_settings_injection(
        self, mock_email_class, mock_render
    ):
        """Test that settings are properly injected into context."""
        # Arrange
        mock_render.side_effect = [
            "Subject",
            "Text content",
            "HTML content",
        ]
        mock_email_instance = Mock()
        mock_email_class.return_value = mock_email_instance

        # Act
        send_email(
            template_name=self.template_name,
            recipients=self.recipients,
            context={"custom": "value"},
        )

        # Assert
        expected_context = {
            "custom": "value",
            "site_url": "https://testdomain.com",
            "project_name": "Test Project",
        }

        for call in mock_render.call_args_list:
            self.assertEqual(call[1]["context"], expected_context)

    @patch("apps.common.services.emails_sending.render_to_string")
    @patch("apps.common.services.emails_sending.EmailMultiAlternatives")
    def test_send_email_empty_recipients_list(
        self, mock_email_class, mock_render
    ):
        """Test email sending with empty recipients list."""
        # Arrange
        mock_render.side_effect = [
            "Subject",
            "Text content",
            "HTML content",
        ]
        mock_email_instance = Mock()
        mock_email_class.return_value = mock_email_instance

        # Act
        send_email(
            template_name=self.template_name,
            recipients=[],  # Empty list
            context=self.context,
        )

        # Assert
        mock_email_class.assert_called_once()
        call_args = mock_email_class.call_args
        self.assertEqual(call_args[1]["to"], [])
        mock_email_instance.send.assert_called_once()
