file_path = 'C:\\Users\\jrben\\OneDrive\\Desktop\\ResumeWork\\walmart_data.csv'
walmart_data = pd.read_csv(file_path)

# Load the data
walmart_data = pd.read_csv(file_path)

# total Revenue
total_revenue = walmart_data['Purchase'].sum()
print(f"Total Revenue: ${total_revenue:,.2f}")

# repeat Purchase Rate
user_purchase_counts = walmart_data['User_ID'].value_counts()
repeat_purchasers = user_purchase_counts[user_purchase_counts > 1].count()
total_unique_users = user_purchase_counts.count()
repeat_purchase_rate = repeat_purchasers / total_unique_users
print(f"Repeat Purchase Rate: {repeat_purchase_rate:.2%}")

# customer lifetime value estimation
clv_per_user = walmart_data.groupby('User_ID')['Purchase'].sum()
average_clv = clv_per_user.mean()
print(f"Average Customer Lifetime Value (CLV): ${average_clv:,.2f}")

# Grouped KPIs by Gender
gender_revenue = walmart_data.groupby('Gender')['Purchase'].sum()
print("\nTotal Revenue by Gender:")
print(gender_revenue)

# Grouped KPIs by Age Group
age_revenue = walmart_data.groupby('Age')['Purchase'].sum()
print("\nTotal Revenue by Age Group:")
print(age_revenue)

# revenue by gender visual
plt.figure(figsize=(8,4))
sns.barplot(x=gender_revenue.index, y=gender_revenue.values, palette="pastel")
plt.title('Total Revenue by Gender')
plt.ylabel('Total Revenue')
plt.xlabel('Gender')
plt.tight_layout()
plt.show()

# revenue by age group visual
plt.figure(figsize=(10,5))
sns.barplot(x=age_revenue.index, y=age_revenue.values, palette="viridis")
plt.title('Total Revenue by Age Group')
plt.ylabel('Total Revenue')
plt.xlabel('Age Group')
plt.tight_layout()

plt.show()
