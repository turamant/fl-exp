function closeNotification(notificationId) {
    const notification = document.querySelector(`div[data-notification-id="${notificationId}"]`);
    notification.remove();
    }

function submitAnswer(button) {
    document.getElementById("answerForm").innerHTML += '<input type="hidden" name="answer" value="' + button.value + '">';
    document.getElementById("answerForm").submit();
}

function checkWordExists(fieldId) {
    const field = document.getElementById(fieldId);
    const feedbackElement = document.getElementById(`${fieldId}-feedback`);
    const submitBtn = document.getElementById('submit-btn');

    fetch(`/check-word?word=${field.value}`)
        .then(response => response.json())
        .then(data => {
            if (data.exists) {
                field.classList.add('is-invalid');
                feedbackElement.textContent = 'This word already exists.';
                feedbackElement.classList.add('invalid-feedback');
                submitBtn.disabled = true;
            } else {
                field.classList.remove('is-invalid');
                feedbackElement.textContent = '';
                feedbackElement.classList.remove('invalid-feedback');
                submitBtn.disabled = false;
            }
        })
        .catch(error => {
            console.error('Error checking word:', error);
            field.classList.remove('is-invalid');
            feedbackElement.textContent = '';
            feedbackElement.classList.remove('invalid-feedback');
            submitBtn.disabled = false;
        });
}

function fadeOutNotifications() {
    var notifications = document.querySelectorAll('.notification');
    notifications.forEach(function(notification, index) {
      setTimeout(function() {
        notification.classList.add('fade-out');
        setTimeout(function() {
          notification.remove();
        }, 1000);
      }, (index + 1) * 1000);
    });
  }

  document.addEventListener('DOMContentLoaded', function() {
    fadeOutNotifications();
  });


function deleteWord(wordId) {
  if (confirm('Вы уверены, что хотите удалить это слово?')) {
      fetch(`/flashcards/delete/${wordId}`, {
          method: 'DELETE',
      })
      .then(response => {
          if (response.ok) {
              const row = document.getElementById(`word_${wordId}`);
              row.remove();
          } else {
              console.error('Ошибка при удалении слова');
          }
      })
      .catch(error => {
          console.error('Ошибка при удалении слова:', error);
      });
  }
}

