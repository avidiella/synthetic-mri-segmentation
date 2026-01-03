# Synthetic Data Generation for MRI Brain Tissue Segmentation
Repository for Data Science master's thesis _Synthetic Data Generation for MRI Brain Tissue Segmentation: An Evaluation of Model Robustness and Generalization_.

![Python](https://img.shields.io/badge/python-3.9%20%E2%80%93%203.12-blue?logo=python&logoColor=white)
![LaTeX](https://img.shields.io/badge/LaTeX-TeX-blueviolet?logo=latex&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=white)
![Conda](https://img.shields.io/badge/Conda-44A833?logo=anaconda&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---
Author: Anna Vidiella de Gonzalo - [avidiellad@uoc.edu](mailto:avidiellad@uoc.edu)

Master's Degree in Data Science, Universitat Oberta de Catalunya

---

## Table of Content
1. [Abstract](#abstract)
2. [About this project](#about-this-project)
   1. [Key Contributions](#key-contributions)
   2. [Project Pipeline](#project-pipeline)
3. [How to cite this work](#how-to-cite-this-work)
4. [References](#references)

---

## Abstract
Deep learning models have been very helpful in the medical field, especially for image analysis tasks such as diagnosis and tissue segmentation. However, their performance requires large, diverse training datasets to achieve good generalization. In the case of brain MRI, the availability of real data can be limited due to cost, patient privacy, or ethical concerns. In this scenario, synthetic data has emerged as an alternative for model training. This master’s thesis proposes the generation of synthetic brain MRI images to evaluate the performance of a deep learning model in tissue segmentation tasks. The images were generated using a generative model that synthesizes MRI scans by sampling from a Gaussian Mixture Model, together with the corresponding segmentation labels for gray matter (GM), white matter (WM), and cerebrospinal fluid (CSF). Domain randomization was implemented to introduce variability in contrast and anatomical shapes, with the aim of improving the model’s generalization. Subsequently, an nnU-Net was trained exclusively on the generated synthetic images, and its performance was evaluated on real brain MRI scans. Although the full training pipeline could not be completed due to time constraints, the results show that the model achieves an acceptable performance, implying that synthetic data can be a viable strategy for model training when real brain MRI images are unavailable. 

**Keywords:** Brain MRI, deep learning, synthetic data, image segmentation, model generalization.

---

## About this project
This work explores the use of synthetic brain MRI data to train a deep learning model for tissue segmentation when real data is limited. A nnU-Net model is trained exclusively on synthetic images and evaluated on real MRI scans from dataset [OASIS-3](https://sites.wustl.edu/oasisbrains/home/oasis-3/) to assess its ability to transfer to real-world data.

The thesis manuscript files can be found in folder [thesis](https://github.com/avidiella/synthetic-mri-segmentation/tree/main/thesis).

### Key Contributions
✅ Proposed a pipeline to generate and pre-process synthetic brain MRI images while implementing domain randomization to improve model generalization. 

✅ Trained a U-Net exclusively on synthetic images.

✅ Evaluated model inferences on real MRI scans, demonstrating good performance for real data.

### Project pipeline
**Data preparation**

For the training set, a total of 500 synthetic brain MRI images, along with corresponding segmentation masks for GM, WM, and CSF, were generated using the `lab2im` library [(Billot et al., 2020)](https://github.com/BBillot/lab2im). The image generation process and the preprocessing steps applied to segmentation masks to adapt the data to the project’s requirements are documented in section [synthetic image generation](https://github.com/avidiella/synthetic-mri-segmentation/tree/main/synthetic-image-generation).

For the test set, 100 real MRI images in the T1w, T2w, and FLAIR sequences were preprocessed to isolate brain tissue from the skull, minimizing potential noise for the model. This preprocessing was performed using the `HD-BET` library [(Isensee et al., 2019)](https://github.com/MIC-DKFZ/HD-BET) and the code developed for these tasks can be found in section [skull-stripping](https://github.com/avidiella/synthetic-mri-segmentation/tree/main/skull-stripping).

To assess the quality of the synthetic MRI, both real images and synthetic images were pre-processed according to the traditional MRI preparation steps detailed in Kondrateva et al. (2024). The different modifications and programs used to perform these changes are detailed in section [image pre-processing](https://github.com/avidiella/synthetic-mri-segmentation/tree/main/image-pre-processing)

**Model developing**
 
The model chosen for this project is `nnU-Net` [(Isensee et al., 2021)](https://doi.org/10.1038/s41592-020-01008-z), a self-configuring, deep learning–based segmentation framework that automatically handles preprocessing, network architecture design, training, and post-processing. All the tasks related to modeling are documented in section [model training](https://github.com/avidiella/synthetic-mri-segmentation/tree/main/model-training)

**Evaluation**

Images were evaluated through both qualitative and quantitative methods. A jupyter notebook showing the results can be found in section [image quality evaluation](https://github.com/avidiella/synthetic-mri-segmentation/tree/main/image-quality-evaluation).

Model results, inference and evaluation documents produced by `nnU-Net` are publicly available in section [model-results](https://github.com/avidiella/synthetic-mri-segmentation/tree/main/model-results).

![segmentation results](https://github.com/avidiella/synthetic-mri-segmentation/blob/main/model-results/segmentation_results.png)

---

## How to cite this work
This code is under a MIT license. If you use it or any part of this work, please cite:

Vidiella-deGonzalo, A. (2025) *Synthetic Data Generation for MRI Brain Tissue Segmentation: An evaluation of model robustness and generalization*. Master's Thesis, Universitat Oberta de Catalunya. Available at: https://github.com/avidiella/synthetic-mri-segmentation.
```
@mastersthesis{VidiellaDeGonzalo2025mri,
  author       = Anna Vidiella-Gonzalo,
  title        = {Synthetic Data Generation for MRI Brain Tissue Segmentation: An evaluation of model robustness and generalization},
  school       = {Universitat Oberta de Catalunya},
  year         = {2025},
  url          = {https://github.com/avidiella/synthetic-mri-segmentation}
}
```

---

## References
* Billot, B., Greve, D., Van Leemput, K., Fischl, B., Iglesias, J.E. and Dalca, A.V., 2020. A learning strategy for contrast-agnostic MRI segmentation. arXiv preprint [arXiv:2003.01995](https://arxiv.org/abs/2003.01995).
* Isensee F., Schell M., Tursunova I., Brugnara G., Bonekamp D., Neuberger U., Wick A., Schlemmer H. P., Heiland S., Wick W., Bendszus M., Maier-Hein K. H., Kickingereder P., 2019. Automated brain extraction of multi-sequence MRI using artificial neural networks. _Human Brain Mapping 40_(17), 4952-4964. https://doi.org/10.1002/hbm.24750
* Isensee, F., Jaeger, P.F., Kohl, S.A., Petersen, J. and Maier-Hein, K.H., 2021. nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation. Nature methods, 18(2), pp.203-211. https://doi.org/10.1038/s41592-020-01008-z
* Kondrateva, E., Druzhinina, P., Dalechina, A., Zolotova, S., Golanov, A., Shirokikh, B., Belyaev, M. and Kurmukov, A., 2024. Negligible effect of brain MRI data preprocessing for tumor segmentation. _Biomedical Signal Processing and Control, 96_, p.106599.
