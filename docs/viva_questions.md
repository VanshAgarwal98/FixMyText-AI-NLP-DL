# Viva Questions and Short Answers

1. **What is NLP?** Natural Language Processing is the field that enables computers to process and analyze human language.
2. **What is text classification?** Assigning a predefined label to a text input.
3. **Why classify complaints?** It helps route reports to relevant departments faster.
4. **What is tokenization?** Splitting text into tokens such as words or subwords.
5. **What is normalization?** Standardizing text while preserving useful meaning.
6. **Why preserve negation?** Words like “not” can reverse a complaint's meaning.
7. **What is TF-IDF?** A representation that weights terms by their importance in a document relative to a corpus.
8. **Why use Logistic Regression?** It is a strong, efficient baseline for sparse text features.
9. **What is an LSTM?** A recurrent neural network architecture designed to model sequence information using gates.
10. **What is a BiLSTM?** An LSTM that processes a sequence in forward and backward directions.
11. **What is an embedding?** A learned dense vector representation of a token.
12. **What is overfitting?** When a model fits training patterns but generalizes poorly to unseen data.
13. **Why split train and test data?** To estimate performance on examples not used for fitting.
14. **What is data leakage?** Using information from outside the training data in a way that inflates evaluation.
15. **Why use macro-F1?** It gives equal weight to each class's F1, useful when classes are imbalanced.
16. **What is a confusion matrix?** A table comparing true and predicted labels.
17. **What does model confidence mean?** A model's predicted probability, not a guarantee of correctness.
18. **Why use SQLite?** It provides simple local persistence without a separate database server.
19. **What is cosine similarity?** A measure of the angle between vector representations.
20. **Does high similarity prove duplicate complaints?** No; it only indicates textual resemblance.
21. **Why map category to department?** It provides a simple, configurable routing suggestion.
22. **Why keep priority rules transparent?** Users and administrators can inspect why a priority was suggested.
23. **What are the dataset limitations?** Small synthetic data may not represent real complaint language.
24. **How can the model improve?** Add diverse labelled data, evaluate errors, and retrain with controlled validation.
25. **What is a model baseline?** A simpler reference model used to compare more complex methods.
26. **Why should humans review low-confidence outputs?** Classification errors can misroute important complaints.
27. **What is early stopping?** Stopping training when validation performance stops improving.
28. **Why not deploy the demo admin toggle?** It does not provide production-grade authentication or authorization.
29. **What is class imbalance?** Some labels have many more examples than others.
30. **What is the project's core contribution?** Combining complaint classification, similarity detection, transparent triage suggestions, and an auditable workflow in a compact application.
