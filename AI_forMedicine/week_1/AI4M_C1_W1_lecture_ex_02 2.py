
# coding: utf-8

# ## AI for Medicine Course 1 Week 1 lecture exercises

# <a name="counting-labels"></a>
# # Counting labels
# 
# As you saw in the lecture videos, one way to avoid having class imbalance impact the loss function is to weight the losses differently.  To choose the weights, you first need to calculate the class frequencies.
# 
# For this exercise, you'll just get the count of each label.  Later on, you'll use the concepts practiced here to calculate frequencies in the assignment!

# In[ ]:


# Import the necessary packages
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# Read csv file containing training datadata
train_df = pd.read_csv("nih/train-small.csv")


# In[ ]:


# Count up the number of instances of each class (drop non-class columns from the counts)
class_counts = train_df.sum().drop(['Image','PatientId'])


# In[ ]:


for column in class_counts.keys():
    print(f"The class {column} has {train_df[column].sum()} samples")


# In[ ]:


# Plot up the distribution of counts
sns.barplot(class_counts.values, class_counts.index, color='b')
plt.title('Distribution of Classes for Training Dataset', fontsize=15)
plt.xlabel('Number of Patients', fontsize=15)
plt.ylabel('Diseases', fontsize=15)
plt.show()


# <a name="weighted-loss"></a>
# # Weighted Loss function
# 

# Below is an example of calculating weighted loss. For this example, you'll first define a hypothetical set of true labels and then a set of random predictions. You'll use the made up examples to practice with the weighted loss function.
# 
# Run the next two cells to create simple examples of labels and predictions

# In[ ]:


# Generate an array of 10 binary label values, 7 positive and 3 negative, then reshape to a column
y_true = np.array([1, 1, 1, 1, 1, 1, 1, 0, 0, 0]).reshape(10, 1)
print(y_true, y_true.shape)


# In[ ]:


# Generate an array of random predictions (either 0 or 0.9 for each) and reshape to a column
y_predict = np.random.randint(0, 2, 10).reshape(10, 1) * 0.9
print(y_predict, y_predict.shape)


# Run the next two cells to define positive and negative weights and a value for epsilon to be used in the loss function.

# In[ ]:


# Define positive and negative weights to be used in the loss function
# The positive weight is determined by the fraction of labels that are negative (3/10 in this case)
positive_weight = 0.3
# The negative weight is determined by the fraction of labels that are positive (7/10 in this case)
negative_weight = 0.7


# In[ ]:


# Define a value "epsilon" to be used in calculating the loss
# This value is just used to avoid an error due to taking the log of zero.
epsilon = 1e-7


# ### Weighted Loss Equation
# Calculate the loss for the zero-th label (column at index 0)
# 
# - The loss is made up of two terms:
#     - $loss_{pos}$: we'll use this to refer to the loss where the actual label is positive (the positive examples).
#     - $loss_{neg}$: we'll use this to refer to the loss where the actual label is negative (the negative examples).  
# - Note that within the $log()$ function, we'll add a tiny positive value, to avoid an error if taking the log of zero.
# 
# $$ loss^{(i)} = loss_{pos}^{(i)} + los_{neg}^{(i)} $$
# 
# $$loss_{pos}^{(i)} = -1 \times weight_{pos}^{(i)} \times y^{(i)} \times log(\hat{y}^{(i)} + \epsilon)$$
# 
# $$loss_{neg}^{(i)} = -1 \times weight_{neg}^{(i)} \times (1- y^{(i)}) \times log(1 - \hat{y}^{(i)} + \epsilon)$$
# 
# $$\epsilon = \text{a tiny positive number}$$
# 
# Run the next three cells to calculate the positive, negative and total loss

# In[ ]:


# Calculate and print out the positive loss
positive_loss = -1 * np.sum(positive_weight * 
                y_true * 
                np.log(y_predict + epsilon)
              )
positive_loss

( -1 * np.log(1- 0.6)) + (  -1 * np.log(1- 0.3))

# In[ ]:


# Calculate and print out the negative loss
negative_loss = -1 * np.sum( 
                negative_weight * 
                (1 - y_true) * 
                np.log(1 - y_predict + epsilon)
              )
negative_loss


# In[ ]:


# Sum positive and negative losses to calculate total loss
total_loss = positive_loss + negative_loss
print(total_loss)


# #### That's all for this lab. You now have a couple more tools you'll need for this week's assignment!
