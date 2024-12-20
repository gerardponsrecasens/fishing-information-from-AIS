## SCRIPT TO IMPLEMENT THE GAMM modeling

library(mgcv)
library(MuMIn)
library(sp)
library(tweedie)

##
# First, VIF is used to reduce the number of columns to which to apply the modeling.
# The columns where Elevation, Week, 11W andCWeekAVG, obtained with the statsmodel in Python.


# import pandas as pd
# import numpy as np
# from statsmodels.stats.outliers_influence import variance_inflation_factor

# def calculate_vif(dataframe):
#     """Calculate Variance Inflation Factor (VIF) for each variable in the DataFrame."""
#     vif_data = pd.DataFrame()
#     vif_data["Variable"] = dataframe.columns
#     vif_data["VIF"] = [
#         variance_inflation_factor(dataframe.values, i) for i in range(dataframe.shape[1])
#     ]
#     return vif_data

# def reduce_multicollinearity(dataframe, threshold=5):
#     """
#     Iteratively remove the variable with the highest VIF
#     until all VIFs are below the threshold.
#     """
#     while True:
#         vif_data = calculate_vif(dataframe)
#         max_vif = vif_data["VIF"].max()
#         if max_vif < threshold:
#             break
#         # Remove the variable with the highest VIF
#         variable_to_remove = vif_data.loc[vif_data["VIF"].idxmax(), "Variable"]
#         dataframe = dataframe.drop(columns=[variable_to_remove])
#         print(f"Removed {variable_to_remove} with VIF {max_vif:.2f}")
#     return dataframe

# # Example usage with your dataset:
# X_train_fish_selected = reduce_multicollinearity(X_train_ais)




###################################################
# USING FISHING DATA IN A CLASSIFICATION SCENARIO #
###################################################
data <- read.csv("fishing.csv")
data$Duration <- log(data$Duration*60)
data$KN <- data$KN/data$Lineas
data$Tag <- data$Tag == "True"

model_fish <- gam(Tag ~
               s(Elevation, k=3) +
               s(Week, k=3) +
               s(X11W, k=3) +
               s(CWeekAvg, k=3) +
               s(Longitude) +
               s(Latitude),
             family = binomial(link = "logit"), 
             data = data, 
             method = "REML")
summary(model_fish)

dredge_results <- dredge(model_fish)
model_fish <- get.models(dredge_results, subset = 1)[[1]]


###################################################
# USING AIS DATA IN A CLASSIFICATION SCENARIO #
###################################################
data <- read.csv("ais.csv")
data$Tag <- data$Tag == "True"
data_clean <- na.omit(data)
model_ais <- gam(Tag ~
               s(Elevation, k=3) +
               s(Week, k=3) +
               s(X11W, k=3) +
               s(CWeekAvg, k=3) +
               s(Longitude) +
               s(Latitude),
             family = binomial(link = "logit"), 
             data = data_clean, 
             method = "REML")
summary(model_ais)

dredge_results <- dredge(model_ais)
model_ais <- get.models(dredge_results, subset = 1)[[1]]

###################################################
# USING JOINED DATA IN A CLASSIFICATION SCENARIO #
###################################################
data <- read.csv("joined.csv")
data$Tag <- data$Tag == "True"
data_clean <- na.omit(data)
model_joined <- gam(Tag ~
               s(Elevation, k=3) +
               s(Week, k=3) +
               s(X11W, k=3) +
               s(CWeekAvg, k=3) +
               s(Longitude) +
               s(Latitude),
             family = binomial(link = "logit"), 
             data = data_clean, 
             method = "REML")
summary(model_joined)


dredge_results <- dredge(model_joined)
model_ais <- get.models(dredge_results, subset = 1)[[1]]


test <- read.csv("test.csv")
test$KN <- test$KN == "True"

test$predicted_prob <- predict(model_fish, newdata = test, type = "response")
test$result <- test$predicted_prob > 0.5
write.csv(test, file = "results_fish.csv", row.names = FALSE)
accuracy_fish <- mean(test$KN == test$result)
precision_fish <- sum(test$KN == TRUE & test$result == TRUE) / sum(test$result == TRUE)
TP <- sum(test$KN == TRUE & test$result == TRUE)  # True Positives
FP <- sum(test$KN == FALSE & test$result == TRUE)  # False Positives
FN <- sum(test$KN == TRUE & test$result == FALSE)  # False Negatives
TN <- sum(test$KN == FALSE & test$result == FALSE)  # True Negatives
recall_fish <- TP / (TP + FN)
f1_fish <- 2 * (precision_fish * recall_fish) / (precision_fish + recall_fish)

test$predicted_prob <- predict(model_ais, newdata = test, type = "response")
test$result <- ifelse(test$predicted_prob > 0.7, TRUE, FALSE)
write.csv(test, file = "results_ais.csv", row.names = FALSE)
accuracy_ais <- mean(test$KN == test$result)
precision_ais <- sum(test$KN == TRUE & test$result == TRUE) / sum(test$result == TRUE)
TP <- sum(test$KN == TRUE & test$result == TRUE)  # True Positives
FP <- sum(test$KN == FALSE & test$result == TRUE)  # False Positives
FN <- sum(test$KN == TRUE & test$result == FALSE)  # False Negatives
TN <- sum(test$KN == FALSE & test$result == FALSE)  # True Negatives
recall_ais <- TP / (TP + FN)
f1_ais <- 2 * (precision_ais * recall_ais) / (precision_ais + recall_ais)

test$predicted_prob <- predict(model_joined, newdata = test, type = "response")
test$result <- test$predicted_prob > 0.5
write.csv(test, file = "results_joined.csv", row.names = FALSE)
accuracy_join <- mean(test$KN == test$result)
precision_join <- sum(test$KN == TRUE & test$result == TRUE) / sum(test$result == TRUE)
TP <- sum(test$KN == TRUE & test$result == TRUE)  # True Positives
FP <- sum(test$KN == FALSE & test$result == TRUE)  # False Positives
FN <- sum(test$KN == TRUE & test$result == FALSE)  # False Negatives
TN <- sum(test$KN == FALSE & test$result == FALSE)  # True Negatives
recall_join <- TP / (TP + FN)
f1_join <- 2 * (precision_join * recall_join) / (precision_join + recall_join)

cat("Accuracy Fish:", accuracy_fish, "\n")
cat("Precision Fish:", precision_fish, "\n")
cat("Recall Fish:", recall_fish, "\n")
cat("F1 Fish:", f1_fish, "\n")
cat("Accuracy AIS:", accuracy_ais, "\n")
cat("Precision AIS:", precision_ais, "\n")
cat("Recall AIS:", recall_ais, "\n")
cat("F1 AIS:", f1_ais, "\n")
cat("Accuracy Joined:", accuracy_join, "\n")
cat("Precision Joined:", precision_join, "\n")
cat("Recall Joined:", recall_join, "\n")
cat("F1 Joined:", f1_join, "\n")