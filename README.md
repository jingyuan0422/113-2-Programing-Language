# Programming Language
* 姓名：黃靖媛
* 授課教師: 蔡芸琤老師


## Homework
### HW1
* [Coding](HW1/HW1.ipynb)

This program automatically generates travel itineraries for the Greater Taipei area. By entering the number of travel days (1–5), users receive optimized daily schedules tailored to attraction types and locations.

### HW2
* [Coding](HW2/HW2.ipynb)
* **Chart 1: Contributions to the Change in Global Mean Surface Temperature (1850–2023)**  

  This line chart illustrates the percentage contributions of major countries to global mean surface temperature change from 1850 to 2023. It reflects long-term trends in global warming responsibility. In recent years, the United States’ contribution has declined to 17.24% in 2023. Meanwhile, China’s share has steadily increased, reaching 12.94%, making it the second-largest contributor.
![圖片名稱](HW2/chart1_LineGraph.png)

* **Chart 2 & 3: 2023 CO₂ Emissions by Country (Bar Chart and Pie Chart)**  

  These charts present both the total CO₂ emissions and each country's share in 2023. China is the largest emitter with 11.9 billion tons, followed by the U.S. (4.9 billion tons) and India (3.1 billion tons). The pie chart shows their respective global shares: China (31.5%), the U.S. (13%), and India (8.1%). Together, these three countries account for over half of global emissions, highlighting the disproportionate impact of a few nations.
![圖片名稱](HW2/chart2_BarChart.png)
![圖片名稱](HW2/chart3_PieChart.png)

* **Chart 4: Scatter Plot – GDP vs CO₂ Emissions by Country**  

  This chart explores the relationship between GDP per capita and total annual CO₂ emissions. The United States shows high GDP per capita with substantial emissions. China, despite lower GDP per capita, has the highest total emissions. India, with low GDP per capita, also emits a significant amount. The chart suggests that both economic output and population size influence emissions, not just wealth alone.
![圖片名稱](HW2/chart4_ScatterPlot.png)

### HW3
* [Coding](HW3/HW3.ipynb)
![圖片名稱](HW3/KMeans_PCA.png)

- **KMeans Analysis**

  **1. Cluster 0** (Upper‑right)  
    - Stocks here score high on both PCA1 and PCA2, meaning they offer high returns and strong risk‑adjusted performance (Sharpe) but come with large price swings and high trading volume.  
    - Examples: NaN
    - Suggested Investment Style: Aggresive (high‑risk, high‑reward)
    - Investor fit: Those willing to tolerate big ups and downs for the chance of outsized gains.

  **2. Cluster 1** (Lower‑left)  
    - These stocks exhibit low returns, low volatility, low Sharpe, and low volume—characteristics of stable, capital‑preserving investments.  
    - Examples: JNJ, UNH
    - Suggested Investment Style: Defensive (low‑risk, stable)
    - Investor fit: Risk‑averse investors seeking minimal price fluctuation.

  **3. Cluster 2** (Lower‑right)  
    - High risk‑adjusted returns (PCA1) paired with moderate‑to‑low volatility and volume.  
    - Examples: NVDA, TSLA, AVGO
    - Suggested Investment Style: Balanced (controlled risk, good return)
    - Investor fit: Those seeking a middle ground—solid returns without extreme risk.

  **4. Cluster 3** (Upper‑left)  
    - These stocks have high volatility and trading activity (PCA2) but only average returns and Sharpe.  
    - Examples: WMT, COST, TMUS
    - Suggested Investment Style: Speculative (high‑volatility plays)
    - Investor fit: Short‑term traders or speculators looking to capitalize on volatility rather than steady performance.

- **Patterns Across PCA Dimensions**
  - PCA1 captures risk-adjusted return (Sharpe) and overall return, while PCA2 reflects volatility and trading volume.
  - Cluster positions in the PCA space help interpret trade-offs: Clusters in the right half lean toward better returns, while those in the upper half show more volatility.

- **Potential Investment Applications**
  - **Portfolio construction:** These clusters can guide allocation strategies—e.g., balancing Cluster 2 (balanced growth) with Cluster 1 (defensive stability).
  - **Risk segmentation:** Traders can focus on Cluster 3 for volatility plays, while long-term investors avoid it due to inconsistent performance.
  - **Strategy matching:** The PCA+KMeans combo helps align stock selection with investor profiles more systematically than traditional sorting.

- **Conclusion**  

  The KMeans clustering successfully grouped stocks into four distinct investment styles—aggressive, defensive, balanced, and speculative. Each cluster shows clear differences in return, volatility, and risk-adjusted performance. These insights can help investors match their risk preferences with the right stock group and build more targeted, diversified portfolios.


***


## Final Project--ResuAI 智慧履歷分析平台
* [第一次提案審查](https://youtu.be/wCUb0VOu1YE)


