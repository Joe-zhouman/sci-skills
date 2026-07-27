# Response Letter #1 — text extraction (for phrasebank mining)

> Text-extracted from `response.pdf` (the authoritative artifact). This `.md`
> exists so `scripts/extract_phrases.py` can grep it — the PDF itself is for
> humans. Source: a real, accepted revision (Nature Communications family /
> Communications Engineering, COMMSENG-25-0150-T). Public.

## Response Letter #1

Dear Editors and Reviewers,

Thank you for your letter and the constructive feedback on our manuscript. We sincerely appreciate the time and effort you have dedicated to evaluating our work and providing insightful suggestions to improve its quality.

We are grateful to the reviewers for their thorough and thoughtful comments, which have helped us refine the methodology, clarify key arguments, and strengthen the overall presentation of the paper. We have carefully addressed all concerns raised in the review reports and incorporated the suggested revisions into the revised manuscript.

## Reviewer #1:

1. Please provide nomenclature for the symbols and abbreviations used.

We sincerely thank the reviewer for pointing out the need to clarify the symbols and abbreviations used in the manuscript. To enhance clarity and accessibility, we will include a dedicated Nomenclature section in the revised version.

2. All figure captions are very detailed. Those should be written in brief while the details about the figures may be discussed in the body text citing the figure.

We thank the reviewer for highlighting the need to streamline our figure captions. In response, we will revise all figure captions to ensure they are succinct and primarily serve to identify the figure's content and purpose.

3. The theoretical model used for data generation is an important part of the present study; therefore, it should be explained in detail in the manuscript.

We appreciate the reviewer's comment regarding the need for a detailed explanation of the theoretical model used for data generation in our study. In response to this feedback, we have incorporated the theoretical model into the Methods section of the manuscript. Given that the theoretical model is not original to this work, we have chosen to present only the essential computational formulas necessary for result reproduction, rather than detailing the full derivation process.

4. Please provide the reference of the thermomechanical properties of 316 stainless steel.

The microhardness data, converted from Vickers hardness, were obtained from Reference [1]. Data for elastic modulus, Poisson's ratio, and thermal conductivity were provided by the specimen supplier. Using literature values leads to slightly larger actual contact areas and smaller contact thermal resistance values compared to our calculations. Specifically, the actual contact area exhibits a relative difference of -2.5% to -1%, while contact thermal resistance shows a discrepancy of approximately 6.868%.

**We contend that this systematic discrepancy—either a uniform increase or decrease—does not undermine the core conclusions of this paper.**

5. How is TCR calculated experimentally, and what are the experimental uncertainties?

The TCR is experimentally determined by the steady-state method based on ASTM D5470. The uncertainty is 5.79%-8.81% for our experiment.

6. Only contact pressure and roughness are considered as parameters affecting thermal contact resistance, not mechanical properties. Therefore, results of the present study will not be valid for other materials?

Under the current framework, predicting TCR for new materials or operating conditions would require generating new datasets and retraining the model. This limitation is indeed inherent to the present work, as discussed in detail in the Discussion section of the manuscript. However, we note that **the costs associated with this retraining process are manageable within practical engineering contexts**, as detailed in the Supplementary Discussion 1. **The modular design of our approach allows for systematic extension to include additional parameters, such as mechanical properties, in future studies.**

7. Line 320: "Both groups exhibit a surface roughness of approximately 0.8." What is this roughness: RMS, Ra, or Rz? And what is the unit?

The surface roughness value of 0.8 refers to the arithmetic mean roughness (Ra), and the unit is microns (μm).

8. Contact thermal resistance is measured experimentally under pressures ranging from 1 to 4.55 MPa, while prediction is for 1 to 10 MPa. Why not in the same pressure range?

Our deep learning model was developed and trained based on a dataset generated from the surface fractal model, which was originally validated over the pressure range of 1–10 MPa. The experimental validation was conducted using our current testing setup, which has a practical pressure limit of approximately 5 MPa due to hardware constraints.

**This inconsistency arises not from any flaw in the methodology, but rather from the temporal sequence of model development and experimental validation — the model was built and trained before the experimental setup was finalized.** We believe that despite this mismatch, the experimental results within the overlapping pressure range sufficiently validate the model's predictive accuracy under realistic conditions.

9. The percentage increase in contact area with pressure from 1-10 MPa is 0.02% to 0.25% for wire cutting specimens, while it is 0.02% to 0.4% for turning specimens. Explain why.

**To begin, we would like to clarify that the predicted contact area values are theoretical estimates, derived from our surface fractal model and multi-point contact mechanics framework. These values have not been experimentally validated in this study, and as noted in the manuscript, the accuracy of these predictions is limited. Therefore, the observed differences should be interpreted with caution and may not fully reflect realworld behavior.**

10. Line 336: A typo error; figure is written two times.

Thank you for your meticulous identification of the spelling errors in the manuscript. These contents have been moved to the Supplementary Discussion 2.

11. Figs. 5 (d, e, f, g, k, l, m, n) have very small texts, so they are not visible.

We have revised all affected panels to ensure all text is now sufficiently large and readable. **Considering these results serve as supplementary validations to our core predictive findings, we have strategically relocated the revised figures to Supplementary Figure 1-2.**

12. To understand the significance of your study, it's essential to compare your results with the existing ML-based studies.

**To the best of our knowledge, there are no existing ML models in the literature that directly tackle TCR/TCC estimation using the same material systems as those investigated in this study. To address this gap, our ongoing research, which aims to establish such a framework, has been shared as a preprint on Chinaxiv and is currently undergoing further refinement and peer review.**

While this preliminary work provides contextual baseline insights, it is important to highlight that it remains under peer review and should be considered as a work in progress.

13. Discuss the limitations of the present study and the techniques used.

Acquisition of datasets: The surface patterns generated via fractal theory exhibit excessive homogeneity in the training dataset, which may lead the neural network to overfit to these specific surface configurations.

Selection of description sets: The current description set is narrowly confined to pressure parameters and surface topography metrics, restricting the model's predictive capability to a single material type.

Experimental validation: this study's empirical verification was limited to contact thermal resistance measurements, with no direct validation of predicted actual contact area values. **Consequently, the model's contact area predictions should be interpreted as approximate estimates rather than definitive measurements.**

## Reviewer #2:

- The process for generating the dataset could be elaborated.

For convenience, we assume that both contacting surfaces have the same fractal dimension. This assumption ensures two rough surfaces can be easily convert to one rough surface and one completely smooth surface.

- Among ResNet, DenseNet, and VGG, why did the authors choose DenseNet121?

Our selection of DenseNet121 as the model demonstrates no particular preference. In fact, to streamline our workflow, we initially planned to experiment with all built-in vision models available in PyTorch. **DenseNet121 was prioritized for preliminary testing due to its alphabetical order in the model nomenclature.** Fortunately, it exhibited promising performance during initial validation, which led to its adoption as the feature extractor in this study.

- The authors highlight the computational efficiency of their model post-training compared to finite element simulations. Quantify these efficiencies.

For the surface topography dataset of size 1024×1204, the FEM requires approximately 7 hours to complete a single prediction of TCR. In contrast, after training, our DL model achieves one-second inference time per prediction, **representing a 25,200-fold acceleration.**

- In Figures 5 and 6, more detailed experimental results should be presented.

Regarding Figure 6 (now revised as Figure 3): We acknowledge the reviewer's concern about the lack of direct experimental validation for this figure. Due to the current testing equipment limitations and the high integration level of the test specimens, it is not feasible to rotate the actual samples for further experimental verification.

**If the reviewer believes that only experimentally validated results should be included in the manuscript, we are happy to remove the related discussion on rotational consistency in the revision to ensure all presented findings are fully supported by experimental data, and the rotational analysis would be discussed in the supplementary.**

- The authors used stainless steel 316 exclusively for validation. How would the analysis hold if the material were changed?

We emphasize that **the associated costs of retraining are practical and feasible within engineering workflows**, as elaborated in the Supplementary Discussion 1. **The modular design of our approach ensures that the framework can be systematically extended to incorporate additional materials or parameters in future studies.**
