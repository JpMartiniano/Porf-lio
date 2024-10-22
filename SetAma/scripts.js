const myObserver = new IntersectionObserver((entries) => {
    entries.forEach( (entry) => {
        if(entry.isIntersecting == true){
            entry.target.classList.add('show')
        } else {
            entry.target.classList.remove('show')
        }
    })
})

// Use querySelectorAll para pegar todos os elementos com a classe 'hidden'
const elements = document.querySelectorAll('.hidden')

// Agora você pode usar forEach com 'elements'
elements.forEach((element) => myObserver.observe(element))

// Array de frases
const phrases = [
    "Você é importante!",
    "Como está sua saúde mental?",
    "Estamos aqui para ajudar!",
    "Valorize a vida!",
    "Converse com alguém de confiança!"
];

let phraseIndex = 0;
let letterIndex = 0;
let isDeleting = false;
const typingSpeed = 80;

function typeEffect() {
    const typingElement = document.querySelector('.typing-effect');
    const currentPhrase = phrases[phraseIndex];

    if (!isDeleting) {
        // Digitação
        typingElement.textContent = currentPhrase.substring(0, letterIndex);
        letterIndex++;

        if (letterIndex > currentPhrase.length) {
            // Pausa ao final da frase
            isDeleting = true;
            setTimeout(typeEffect, 2000); // Pausa de 2 segundos
        } else {
            setTimeout(typeEffect, typingSpeed);
        }
    } else {
        // Exclusão
        typingElement.textContent = currentPhrase.substring(0, letterIndex);
        letterIndex--;

        if (letterIndex === 0) {
            isDeleting = false;
            phraseIndex++;
            if (phraseIndex >= phrases.length) {
                phraseIndex = 0;
            }
            setTimeout(typeEffect, 500); // Pausa antes de começar a digitar a próxima frase
        } else {
            setTimeout(typeEffect, typingSpeed);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    typeEffect();
});

// Mostrar navbar ao rolar a página
window.addEventListener('scroll', () => {
    const header = document.getElementById('main-header');
    if (window.scrollY > header.offsetHeight - 100) {
        document.body.classList.add('scrolled');
    } else {
        document.body.classList.remove('scrolled');
    }
});

const quizData = [
    {
        question: "O que você deve fazer ao perceber que alguém está passando por um momento difícil?",
        options: [
            "Evitar a pessoa para não piorar a situação.",
            "Oferecer seu apoio e escutar sem julgamentos.",
            "Dizer que ela deve superar sozinha."
        ],
        correct: 1
    },
    // Adicione mais 9 perguntas aqui
    {
        question: "Qual a melhor forma de iniciar uma conversa sobre saúde mental?",
        options: [
            "Expressar preocupação genuína e perguntar como a pessoa está se sentindo.",
            "Ignorar os sinais e esperar que a pessoa fale primeiro.",
            "Fazer piadas para aliviar o clima."
        ],
        correct: 0
    },
    {
        question: "O que NÃO é recomendado ao oferecer suporte?",
        options: [
            "Minimizar os sentimentos da pessoa.",
            "Ouvir atentamente.",
            "Encaminhar para ajuda profissional."
        ],
        correct: 0
    },
    {
        question: "Qual desses é um sinal de que alguém pode precisar de ajuda?",
        options: [
            "Mudanças bruscas de humor.",
            "Interesse em novas atividades.",
            "Socialização com amigos."
        ],
        correct: 0
    },
    {
        question: "Como o apoio contínuo pode beneficiar alguém em crise?",
        options: [
            "Demonstra que a pessoa não está sozinha.",
            "Faz com que a pessoa dependa totalmente de você.",
            "Não tem impacto significativo."
        ],
        correct: 0
    },
    {
        question: "Por que é importante evitar frases clichês?",
        options: [
            "Porque podem minimizar os sentimentos da pessoa.",
            "Porque mostram compreensão.",
            "Porque incentivam a pessoa a falar mais."
        ],
        correct: 0
    },
    {
        question: "Qual é o número do CVV (Centro de Valorização da Vida)?",
        options: [
            "188",
            "190",
            "192"
        ],
        correct: 0
    },
    {
        question: "O que fazer se alguém recusar ajuda profissional?",
        options: [
            "Respeitar a decisão e continuar oferecendo apoio.",
            "Forçar a pessoa a ir ao médico.",
            "Abandonar a pessoa."
        ],
        correct: 0
    },
    {
        question: "Qual é uma forma eficaz de mostrar empatia?",
        options: [
            "Compartilhar suas próprias experiências sem ouvir a pessoa.",
            "Validar os sentimentos da pessoa e oferecer suporte.",
            "Dizer que poderia ser pior."
        ],
        correct: 1
    },
    {
        question: "Por que é importante cuidar da sua própria saúde mental ao ajudar alguém?",
        options: [
            "Para garantir que você esteja em condições de oferecer suporte.",
            "Não é importante.",
            "Porque mostra fraqueza."
        ],
        correct: 0
    }
];

const quizContainer = document.getElementById('quiz-container');

function loadQuiz() {
    quizData.forEach((quizItem, index) => {
        const questionEl = document.createElement('div');
        questionEl.classList.add('question');

        const questionTitle = document.createElement('h3');
        questionTitle.textContent = `Pergunta ${index + 1}`;
        questionEl.appendChild(questionTitle);

        const questionText = document.createElement('p');
        questionText.textContent = quizItem.question;
        questionEl.appendChild(questionText);

        const optionsList = document.createElement('ul');
        optionsList.classList.add('options');

        quizItem.options.forEach((optionText, optionIndex) => {
            const optionEl = document.createElement('li');
            optionEl.classList.add('option');
            optionEl.textContent = optionText;
            optionEl.addEventListener('click', () => selectOption(optionEl, quizItem.correct, optionIndex));
            optionsList.appendChild(optionEl);
        });

        questionEl.appendChild(optionsList);
        quizContainer.appendChild(questionEl);
    });
}

function selectOption(optionEl, correctAnswer, selectedAnswer) {
    if (optionEl.classList.contains('answered')) return;

    if (selectedAnswer === correctAnswer) {
        optionEl.classList.add('correct');
        showModal('Parabéns! Você acertou a resposta!');
    } else {
        optionEl.classList.add('incorrect');
        showModal('Resposta incorreta. Tente novamente!');
    }

    optionEl.classList.add('answered');
}

function showModal(message) {
    const modal = document.getElementById('modal');
    const modalMessage = document.getElementById('modal-message');
    modalMessage.textContent = message;
    modal.style.display = 'flex';
}

document.getElementById('close-modal').addEventListener('click', () => {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
});

loadQuiz();

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        if (this.getAttribute('href') !== '#') {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 60; // Altura da navbar em pixels
                const elementPosition = target.offsetTop;
                const offsetPosition = elementPosition - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        }
    });
});