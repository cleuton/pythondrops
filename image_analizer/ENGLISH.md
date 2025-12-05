![](./real_fake.png)

# Is it real or fake? 

This code works as an “image detective” that looks for statistical clues to determine whether a picture was created by a real camera or by AI.

Limitations
It is not infallible: Accuracy is lower than modern neural-network-based detectors, but it is much simpler and requires far less hardware.
It is sensitive to edits: Compression or filters can erase the clues.
Rapid evolution of AI: New models generate increasingly realistic images.
It serves as a first analysis layer — a “statistical fine-comb” for initial triage, prioritizing simplicity and transparency.

Techniques
It uses four main techniques and a classifier, following this flow:

1. Residual Noise Analysis
   It applies a smoothing filter to the image and compares it with the original, because the difference between them reveals the “residual noise” (small natural imperfections).

Real cameras leave a unique noise pattern (like the sensor’s “fingerprint”).
AI-generated images have more artificial or uniform noise (a texture that is “too perfect”).

2. Frequency Analysis
   The image is divided into blocks, and the distribution of fine details (high frequencies) versus smooth areas (low frequencies) is analyzed.

Real images contain many microscopic details (hair, grains of sand).
AI images may lose these details or show repetitive patterns (blurred lines, unnatural textures).

3. Color Analysis
   It analyzes color statistics (mean, variance, skewness) across three channels: luminance (Y), blue (Cb), and red (Cr).

Real cameras capture colors with natural and imperfect variations.
AI images may show overly smoothed colors or artificially concentrated tones (like leaf greens that are “too perfect”).

4. Texture Analysis
   It uses the LBP algorithm to map local texture patterns (lines, curves, points) and builds a histogram of those patterns.

Real textures are varied and complex (human skin, fabric).
AI images may have repetitive or simplified patterns (a “cloned” fabric texture appearing across the image).

5. Final Classifier
   All extracted clues are combined into a feature list, and a Logistic Regression model is trained to learn the difference between real and AI images, producing a probability (%) that an image is artificial.

Logistic Regression is simple, fast, and explainable — ideal for understanding which features matter most.

Complete Pipeline
Data Collection: A labeled dataset (“real” vs. “AI”) is loaded.
Feature Extraction: Each image goes through the four analyses, producing a “statistical profile.”
Training: The model learns to associate these profiles with their labels.
Prediction: New images are analyzed and receive a probability of being AI.

Why These Techniques Work
AI images, even highly realistic ones, still make subtle statistical “mistakes” that humans overlook but algorithms detect:

Artificial noise: Lack of the natural camera “fingerprint.”
Missing micro-details: Simplified complex textures.
Colors that are “too perfect”: Unusual tone distributions.
Repetitive patterns: Cloned or symmetric textures.

How to Use
A directory contains several AI-generated images, photos I took myself, and free images from Pixabay. Just run the program. At the end, it will test the generated model with 2 real and 2 AI images.

For “production” use, save the generated model.

How to Improve
Use more images. The training/testing dataset is small. Test with at least 200 images: 100 real and 100 AI (roughly matching real photos).

Try additional noise filters (Wavelet, Median) beyond bilateral.
Add entropy to the residual-noise statistics to measure complexity.
Replace FFT with DCT in frequency analysis.
Use edge masks (Canny) before spectral analysis.
Expand color analysis to HSV or LAB spaces.
Balance the dataset (equal numbers of real and AI images).
Switch to an RBF-kernel SVM to capture nonlinear patterns.

---

If you want, I can also rewrite this into documentation format (README), technical article style, or a simplified explanation for non-technical users.
