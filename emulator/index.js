let answered = false

function updateQuestion(q) {
    document.getElementById('question').innerHTML = q.results[0].question;
    Array.from(document.getElementsByClassName('reaction')).forEach((reaction) => {
    reaction.dataset.selected = 'no'
    console.log(reaction)
    toggleSelect = () => {
        if (reaction.dataset.selected == 'no') {
            reaction.dataset.selected = 'yes'
            if (!answered) {
                answered = true
                setTimeout(() => {
                    document.getElementById('question-name').innerHTML = 'Answer'
                    if (reaction.dataset.value == q.results[0].correct_answer) {
                        document.getElementsByClassName('reaction-container')[0].innerHTML = '<span class="reaction"><img draggable="false" class="emoji " alt="✅" title=":white_check_mark:" src="https://twemoji.maxcdn.com/2/svg/2705.svg"></span>'
                        document.getElementById('question').innerHTML = 'You were correct! Good job!'
                    } else {
                        document.getElementsByClassName('reaction-container')[0].innerHTML = '<span class="reaction"><img draggable="false" class="emoji " alt="❌" title=":x:" src="https://twemoji.maxcdn.com/2/svg/274c.svg"></span>'
                        document.getElementById('question').innerHTML = 'You were incorrect! Nice try!'
                    }
                }, 800)
            }
        } else {
            reaction.dataset.selected = 'no'
        }
    }
    reaction.addEventListener('click', toggleSelect)
})
}

const xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      updateQuestion(JSON.parse(this.responseText));
    }
  };
xhttp.open('GET', 'https://opentdb.com/api.php?amount=1&difficulty=easy&type=boolean')
xhttp.send()