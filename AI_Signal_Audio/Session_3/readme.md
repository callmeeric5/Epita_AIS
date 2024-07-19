# Spectrogram-Based Music Genre Classification CNN

In this assignment, I have tried several ways to build and train the model

## Conv=7, lr=0.0001, ReduceLROnPlateau(factor=0.3, patience=10), EarlyStopping(patience=15)
Validation Loss: 0.40432727336883545
Validation Accuracy: 0.8333333134651184

![image](https://github.com/user-attachments/assets/f5c40433-bc55-4731-b583-67621531121a)



## Conv=7, lr=0.0001
Validation Loss: 0.45307597517967224
Validation Accuracy: 0.8333333134651184

![image](https://github.com/user-attachments/assets/e4b671bb-7593-4886-8b80-25f07b4fe338)


## Conv=3, lr=0.001, ReduceLROnPlateau(factor=0.5, patience=15), EarlyStopping(patience=20)
Validation Loss: 0.37062695622444153
Validation Accuracy: 0.8666666746139526

![image](https://github.com/user-attachments/assets/eb4de372-504c-4747-9ed9-41ef36a8e2df)


## Conv=5, lr=0.0001, ReduceLROnPlateau(factor=0.1, patience=5), EarlyStopping(patience=10)
Validation Loss: 0.45689231157302856
Validation Accuracy: 0.800000011920929

![image](https://github.com/user-attachments/assets/30af2b00-a363-43c2-924b-e83fbcd0f5b1)

## Conclusion
1. The third model achieve the best accuracy on the validation data, however, it shows signs of overfitting. Decreasing the EarlyStopping patience to 10 may help adress this problem.
2. From the comparison between the first and second plots, it indicates ReduceLROnPlateau and EarlyStopping can help us solve overfitting problems during training.
3. From From the comparison among the different CNN models with different conv2d sizes, the model accuracy will be influenced by it and the size = 3 is the best for this dataset
4. From the comparison among the different training strategies, the adjust of lr and early stop can help prevent overfitting obviously but the value of parameters will determine how efficent it could help.

## Challenges
I havn't use ReduceLROnPlateau before in my previous projects because Adam dynamically adjusts the learning rate during the training. I thought it is uncecessary to use any lr adjuster but this assignment proved I was wrong.
