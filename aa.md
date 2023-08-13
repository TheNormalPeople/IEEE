---
title :文档质量过滤

---

* we downloaded and filtered a version of CommonCrawl based on similarity to a range of high-quality reference corpora, 
* we performed fuzzy deduplication at the document level, within and across datasets, to prevent redundancy and preserve the integrity of our held-out validation set as an accurate measure of overfitting
* we also added known high-quality reference corpora to the training mix to augment CommonCrawl and increase its diversity.



1. 使用与高质量参考语料库的相似性过滤CommonCrawl。（使用高质量数据作为正例，训练LR分类算法，对 CommonCrawl 的所有文档做初步过滤）
2. 在文档级别，数据集内部和数据集之间使用模糊操作删除重复数据。（利用公开的算法做文档去重，减少冗余数据；）
3. 在训练组合（training mix）中添加已知的高质量参考语料库。（“高质量数据”主要是指 BERT、GPT、GPT-2 使用过的数据，最终处理完成后使用的数据规模约 570G）。



* In order to improve the quality of Common Crawl, we developed an automatic filtering method to remove low quality documents. Using the original WebText as a proxy for high-quality documents, we trained a classifier to distinguish these from raw Common Crawl. We then used this classifier to re-sample Common Crawl by prioritizing documents which were predicted by the classifier to be higher quality. The classifier is trained using logistic regression classifier with features from Spark’s standard tokenizer and HashingTF 10. For the positive examples, we used a collection of curated datasets such as WebText, Wikiedia, and our web books corpus as the positive examples, and for the negative examples, we used unfiltered Common Crawl. We used this classifier to score Common Crawl documents. We kept each document in our dataset iff

  ​																				$$np.random.pareto(\alpha) > 1 -document_score$$

  We chose $\alpha$ = 9 in order to take mostly documents the classifier scored highly, but still include some documents that were out of distribution. $\alpha$ was chosen to match the distribution of scores from our classifier on WebText. We found this re-weighting increased quality as measured by loss on a range of out-of-distribution generative text samples.

  使用WebText、Wikiedia和网络书籍语料库作为正样本，使用未经过滤的Common Crawl作为负样本。训练一个逻辑回归分类器，该分类器具有Spark的 standard tokenizer和HashingTF 10。

  选择$\alpha$ = 9是为了获取分类器得分很高的文档，但是仍然包括一些分布之外的文档。$\alpha = 9$是为了匹配WebText上分类器的分数分布。

* To further improve model quality and prevent overfitting (which becomes increasingly important as model capacity increases), we fuzzily deduplicated documents (i.e. removed documents with high overlap with other documents) within each dataset using Spark’s MinHashLSH implementation with 10 hashes, using the same features as were used for classification above. We also fuzzily removed WebText from Common Crawl. Overall this decreased dataset size by an average of 10%.

  为了进一步提高模型质量和防止过度拟合，使用Spark的MinHashLSH具有10哈希（10 hashes）的实现，使用与上面相同的特征在每个数据集中模糊地删除文档（删除与其他文档高度重叠的文档）。
