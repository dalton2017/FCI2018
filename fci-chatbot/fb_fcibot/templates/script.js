var myQuestions = [
    { 
        question: "What is the capital of Bangladesh?",
        answers: {a: "Dhaka",b: "Chittagong",c: "Sylhet"
        },
        correctAnswer: "a"
    },
    { 
        question: "What does 2+2 equal to?",
        answers: {a:"3", b:"2", c:"4"},
        correctAnswer: "c"
    },
    { 
        question: "What is the real name of Damon Salvatore?",
        answers: {a:"Paul Wesley", b:"Steven McQueen",c: "Ian Somerhalder"}, 
        correctAnswer:"c"
    },
    { 
        question: "What is the name of the largest planet in the universe?",
        answers: {a:"Earth", b:"Jupiter", c:"Uranus"},
        correctAnswer: "b"
    },
    { 
        question: "What is the capital of New York?",
        answers: {a:"Manhattan", b:"NYC", c:"Albany"},
        correctAnswer:"a"
    },
    { 
        question: "How many bones does the human body have?",
        answers: {a:"109", b:"206", c:"114"},
        correctAnswer: "b"
    },
    { 
        question: "What is the alter ego of Batman?",
        answers: {a:"Bruce Banner", b:"Bruce Wayne", c:"Tony Stark"},
        correctAnswer: "a"
    },
    { 
        question: "How many books are there in the Harry Potter series?",
        answers: {a:"7", b:"5",c: "8"},
        correctAnswer: "a"
    },
    { 
        question: "What is Naruto's surname?",
        answers: {a:"Sarutobi", b:"Uchiha", c:"Uzumaki"},  
        correctAnswer: "c"
    },
    { 
        question: "What is the name of Sherlock Holmes' partner?",
        answers: {a:"Peterson", b:"Watson",c: "Hanson"},  
        correctAnswer: "b"
    }

];

function buildQuiz() {
    var output = [];

    myQuestions.forEach((currentQuestion, questionNumber) => {
        var answers = [];

        for (letter in currentQuestion.answers) {
        answers.push(
          `<label>
             <input type="radio" name="question${questionNumber}" value="${letter}">
              ${letter} :
              ${currentQuestion.answers[letter]}
           </label>`
        );
        }

        output.push(
        `<div class="slide">
           <div class="question"> ${currentQuestion.question} </div>
           <div class="answers"> ${answers.join("")} </div>
         </div>`
        );
        });

    quizContainer.innerHTML = output.join("");
}

function showResults() {
    var answerContainers = quizContainer.querySelectorAll(".answers");

    let numCorrect = 0;

    myQuestions.forEach((currentQuestion, questionNumber) => {
        var answerContainer = answerContainers[questionNumber];
        var selector = `input[name=question${questionNumber}]:checked`;
        var userAnswer = (answerContainer.querySelector(selector) || {}).value;

        if (userAnswer === currentQuestion.correctAnswer) {
        numCorrect++;

        answerContainers[questionNumber].style.color = "lightgreen";
        } else {
        answerContainers[questionNumber].style.color = "red";
        }
        });

    resultsContainer.innerHTML = `${numCorrect} out of ${myQuestions.length}`;
}

function showSlide(n) {
    slides[currentSlide].classList.remove("active-slide");
    slides[n].classList.add("active-slide");
    currentSlide = n;

    if (currentSlide === 0) {
        previousButton.style.display = "none";
    } 
    else {
        previousButton.style.display = "inline-block";
    }

    if (currentSlide === slides.length - 1) {
        nextButton.style.display = "none";
        submitButton.style.display = "inline-block";
    } 
    else {
        nextButton.style.display = "inline-block";
        submitButton.style.display = "none";
    }
}

function showNextSlide() {
    showSlide(currentSlide + 1);
}

function showPreviousSlide() {
    showSlide(currentSlide - 1);
}

var quizContainer = document.getElementById("quiz");
var resultsContainer = document.getElementById("results");
var submitButton = document.getElementById("submit");

buildQuiz();

var previousButton = document.getElementById("previous");
var nextButton = document.getElementById("next");
var slides = document.querySelectorAll(".slide");
let currentSlide = 0;

showSlide(0);
submitButton.addEventListener("click", showResults);
previousButton.addEventListener("click", showPreviousSlide);
nextButton.addEventListener("click", showNextSlide);