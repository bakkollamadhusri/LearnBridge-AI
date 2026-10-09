import uuid
from typing import List, Dict, Any
from ..models import Flashcard, PracticeQuestion, QuizResult

class QuizService:
    @staticmethod
    def generate_flashcards(topic: str, count: int = 5) -> List[Flashcard]:
        topic_lower = topic.lower()
        cards = []

        if "machine learning" in topic_lower or "ml" in topic_lower or "ai" in topic_lower:
            raw = [
                ("What is Supervised Learning?", "A machine learning paradigm where the algorithm is trained on labelled input-output training pairs.", "AI/ML"),
                ("What is Overfitting?", "When a model learns the training noise too closely, failing to generalize to unseen test data.", "Model Evaluation"),
                ("What is the function of Gradient Descent?", "An optimization algorithm that iteratively adjusts model parameters to minimize loss.", "Optimization"),
                ("What is Unsupervised Learning?", "Discovering patterns, clusters, and representations in data without predefined labels.", "AI/ML"),
                ("What is Cross-Validation?", "A statistical technique (e.g. K-fold) to assess how well a model generalizes to independent datasets.", "Validation")
            ]
        elif "diode" in topic_lower or "semiconductor" in topic_lower:
            raw = [
                ("What is the Depletion Region?", "An insulating zone around the PN junction depleted of free mobile charge carriers.", "Semiconductors"),
                ("What is Forward Bias?", "Connecting Anode (+) to P-side and Cathode (-) to N-side, overcoming barrier and allowing current.", "Circuits"),
                ("What is the Barrier Voltage of Silicon?", "Approximately 0.7 Volts at room temperature.", "Electronics"),
                ("What is a Rectifier?", "An electrical circuit utilizing diodes to convert alternating current (AC) to direct current (DC).", "Power Electronics"),
                ("What is Zener Breakdown?", "A heavily doped PN junction breakdown occurring under reverse bias due to quantum tunneling.", "Devices")
            ]
        else:
            raw = [
                (f"What is the core purpose of {topic.title()}?", f"{topic.title()} serves to solve domain-specific problems by applying systematic principles.", "Fundamentals"),
                (f"What are the prerequisites for {topic.title()}?", "Understanding basic terminology, foundational theories, and initial constraints.", "Prerequisites"),
                (f"How is {topic.title()} evaluated in practice?", "Through benchmark tests, empirical measurements, and consistency checks.", "Evaluation"),
                (f"What is a common pitfall in {topic.title()}?", "Skipping verification steps and misinterpreting underlying assumptions.", "Best Practices"),
                (f"Where is {topic.title()} applied in industry?", "In automation, production systems, and academic research.", "Applications")
            ]

        for q, a, cat in raw[:count]:
            cards.append(Flashcard(
                id=str(uuid.uuid4())[:8],
                question=q,
                answer=a,
                category=cat,
                mastered=False
            ))
        return cards

    @staticmethod
    def generate_quiz(topic: str) -> List[PracticeQuestion]:
        topic_lower = topic.lower()
        if "machine learning" in topic_lower or "ml" in topic_lower:
            return [
                PracticeQuestion(
                    question="Which evaluation metric is best suited for an imbalanced classification problem?",
                    options=["Accuracy", "F1-Score / Precision-Recall AUC", "Mean Squared Error", "R-Squared"],
                    correct_answer=1,
                    explanation="In imbalanced datasets, overall accuracy can be misleading. F1-score balances precision and recall."
                ),
                PracticeQuestion(
                    question="What role does an activation function play in a neural network?",
                    options=[
                        "It speeds up file downloads",
                        "It introduces non-linearity, allowing the network to learn complex patterns",
                        "It acts as a hardware voltage regulator",
                        "It resets weights to zero after each epoch"
                    ],
                    correct_answer=1,
                    explanation="Without non-linear activations, stacking neural layers would just equal a single linear regression."
                ),
                PracticeQuestion(
                    question="Which clustering algorithm is an example of unsupervised learning?",
                    options=["Support Vector Machine", "K-Means", "Random Forest Classifier", "Logistic Regression"],
                    correct_answer=1,
                    explanation="K-Means groups data into K clusters based on Euclidean distance without using label supervision."
                )
            ]
        elif "diode" in topic_lower:
            return [
                PracticeQuestion(
                    question="In a forward-biased PN junction, current is primarily conducted by:",
                    options=["Majority charge carriers", "Minority charge carriers", "Neutrons", "Immobile ions"],
                    correct_answer=0,
                    explanation="Forward bias pushes majority carriers (holes in P, electrons in N) across the reduced depletion barrier."
                ),
                PracticeQuestion(
                    question="Which diode is specifically designed to operate reliably in the reverse breakdown region?",
                    options=["Schottky diode", "Zener diode", "Photodiode", "Tunnel diode"],
                    correct_answer=1,
                    explanation="Zener diodes maintain a stable breakdown voltage under reverse bias, making them ideal voltage regulators."
                )
            ]
        else:
            return [
                PracticeQuestion(
                    question=f"Which aspect is critical when implementing {topic.title()}?",
                    options=[
                        "Adhering to foundational principles and testing assumptions",
                        "Ignoring edge cases and error bounds",
                        "Never documenting architectural decisions",
                        "Random guessing"
                    ],
                    correct_answer=0,
                    explanation="Foundational understanding and rigorous validation ensure reliable outcomes."
                ),
                PracticeQuestion(
                    question=f"What is the first recommended step in analyzing {topic.title()}?",
                    options=[
                        "Defining requirements, constraints, and inputs",
                        "Skipping straight to final deployment",
                        "Assuming zero dependencies",
                        "Terminating the execution"
                    ],
                    correct_answer=0,
                    explanation="Establishing clear initial conditions and definitions is vital for structured problem solving."
                )
            ]

    @staticmethod
    def evaluate_quiz(quiz_id: str, questions: List[PracticeQuestion], user_answers: Dict[int, int]) -> QuizResult:
        correct = 0
        details = []
        for idx, q in enumerate(questions):
            ans = user_answers.get(idx)
            is_correct = (ans == q.correct_answer)
            if is_correct:
                correct += 1
            details.append({
                "question_index": idx,
                "question": q.question,
                "user_answer": ans,
                "correct_answer": q.correct_answer,
                "is_correct": is_correct,
                "explanation": q.explanation
            })

        total = len(questions)
        pct = round((correct / total) * 100, 1) if total > 0 else 0.0
        
        if pct >= 80:
            feedback = "🌟 Outstanding! You have mastered the core principles of this concept."
        elif pct >= 50:
            feedback = "👍 Good effort! Review the explanations above to strengthen your conceptual grasp."
        else:
            feedback = "📚 Keep going! Revisiting the simple explanation and diagram will boost your score."

        return QuizResult(
            quiz_id=quiz_id,
            total_questions=total,
            correct_count=correct,
            score_percentage=pct,
            feedback=feedback,
            results_detail=details
        )
