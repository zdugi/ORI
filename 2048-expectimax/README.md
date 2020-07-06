# Projekat: 2048 sa agentom korišćenjem expectimax algoritma

Projekat je rađen u Python 3.7.
Za izradu projekta su korišćene reference: 
- Heuristic - https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048 (heuristika)
- 2048 expectimax - https://www.cs.uml.edu/ecg/uploads/AIfall14/vignesh_gayas_2048_project.pdf
- 2048 expectimax python - https://github.com/Lesaun/2048-expectimax-ai (referenti rad)

## Heuristike
Finalna heuristika je smoothness heuristika koja predstavlja razliku između susednih pločica i teži
se njenom smanjivanju, pored toga se gleda i broj praznih pločica kao nagrada i kazna za svaku pločicu koja se pojavljuje više od 2 puta.

Prilikom izrade smo koristili i monotocity heuristiku koja daje negativne bodove za svaki red koji nema monotonost, 
smoothness se bolje pokazao pa smo se odlučili za njega.
