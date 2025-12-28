# -*- coding: cp1252 -*-
# ===============================
# author: Paulo Trigo Silva (PTS)
# version: v01
# ===============================


#______________________________________________________________________________
# The modules to import
from math import sqrt
from random import randrange
from random import seed
import csv
import matplotlib.pyplot as plt



#______________________________________________________________________________
# The base concepts:
# - similarity-criteria
# - attraction/repulsion rules
# - learning-rate

## similarity-criteria
# - computed as the Euclidean distance between two vectors (v1 and v2)
def get_euclidean_distance( v1, v2 ):
  distance = 0.0
  # the feature list excludes last component because it is the "class"
  lenFeature = len(v1) - 1
  for i in range( lenFeature ): 
    distance += (v1[i] - v2[i]) ** 2
    #<HERE> implement the Euclidean distance (recall Spreadsheet exercise)
  return sqrt(distance)


## attraction/repulsion rules
def apply_attraction_rule( learningRate, trainingInstance, BMU ):
  return attraction_repulsion_rule( learningRate, trainingInstance, BMU,
                                    lambda a, b: a + b )


def apply_repulsion_rule( learningRate, trainingInstance, BMU ):
  return attraction_repulsion_rule( learningRate, trainingInstance, BMU,
                                    lambda a, b: a - b )


def attraction_repulsion_rule( learningRate, trainingInstance, BMU,
                               operator ):
  sumError = 0.0
  # the feature list excludes last component because it is the "class"
  lenFeature = len(trainingInstance) - 1
  for i in range(lenFeature):
    error = trainingInstance[i] - BMU[i]
    sumError += error**2
    BMU[i] = operator( BMU[i], learningRate * error )
  return ( BMU, sumError )


## learning-rate (non-linear)
def get_learning_rate( alpha, epoch, maxEpoch ):
  return alpha * ( 1.0 - (epoch / float( maxEpoch ) ))
  #<HERE> return the time-dependent learning rate (cf., slides)
  #return alpha * ( 1.0 <HERE> float( maxEpoch ) ) )



#______________________________________________________________________________
# The algorithm specific methods
#______________________________________________________________________________

# get the BMU - Best Matching Unit
def get_BMU( codebook, trainingInstance ):
  # set BMU to None and minimum distance to Infnity
  ( BMU, minDistance ) = ( None, float( "inf" ) )
  for cBv in codebook:
    distance = get_euclidean_distance( cBv, trainingInstance )
    if( distance <= minDistance ):
      ( BMU, minDistance ) = ( cBv, distance )
  return BMU


# train a codebook, given:
# - a dataset, an initial codebook,
# - the alpha initial-learning-rate and the maximum number of epochs
def train_LVQ( dataset, codebook, alpha, maxEpoch ):
  errors = []
  for epoch in range( maxEpoch ):
    lRate = get_learning_rate( alpha, epoch, maxEpoch )
    totalError = 0.0
    for trainingInstance in dataset:
      BMU = get_BMU( codebook, trainingInstance )
      if BMU[-1] == trainingInstance[-1]:
        ( BMU, error ) = apply_attraction_rule( lRate, trainingInstance, BMU )
      else:
        ( BMU, error ) = apply_repulsion_rule( lRate, trainingInstance, BMU )
      totalError += error

    errors.append(totalError)
    print( "> Epoch=%d, learningRate=%.3f, totalError=%.3f" % \
           (epoch, lRate, totalError))
  return ( codebook, totalError, errors )


#______________________________________________________________________________
# Build a random codebook vector (taken from the dataset)
def build_codebook_random( dataset ):
  lenDataset = len( dataset )
  lenFeature = len( dataset[0] )
  codebook = [ dataset[randrange(lenDataset)][i] for i in range(lenFeature) ]
  return codebook



#______________________________________________________________________________
# Auxiliary Functions

# read csv file
def read_csv( fileName, delimiter=';' ):
  with open( fileName ) as f_in:
   reader = csv.reader( f_in, delimiter=delimiter )
   header = next( reader )
   dataset = list()
   for row in reader:
    # ignore empty lines
    if not row: continue

    row_list = list()
    for col in range(len(row)-1):
      # all features are of continuous type (cast to float)
      row_list.append( float( row[col] ) )
    # the last column is the class of discrete type (cast to string)
    row_list.append( str( row[len(row)-1] ).strip() )
    dataset.append( row_list )
  return ( header, dataset )


# print info
def print_info( description, aHeader, aList, aStr=None, aFloat=None ):
  print()
  print( description )
  print( aHeader )
  for e in aList: print( e )
  if( aStr ): print( aStr, end="" )
  if( aFloat ): print( "{0: .3f}".format( aFloat ), end="\n"*2 )


#______________________________________________________________________________
# The Learning Parameters
#______________________________________________________________________________
seed( 1 )

_alpha = 0.7
_maxEpoch = 100
_codebookRandom = True 
# next variable only used for the random codebook (if _codebookRandom = True):
_dimCodebook = 15
#______________________________________________________________________________


#______________________________________________________________________________
# The Dataset and Codebook files in CSV Format
#______________________________________________________________________________
_datasetFileName_csv  = r"01_dataset_slides.txt" 
_codebookFileName_csv = r"02_codebook_slides.txt"

# Plotting the function 
def plot_error(errors, save_path=None):
  plt.figure(figsize=(10, 6)) 
  plt.plot(errors, label="Total Error", color='blue') 
  plt.xlabel("Epoch") 
  plt.ylabel("Total Error") 
  plt.title("Evolution of Total Error Over Epochs") 
  plt.legend() 
  plt.grid(True)
  if save_path:
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {save_path}")
  plt.show()
  plt.close()


#______________________________________________________________________________
# The "main" function
def main():
  (data_header, dataset) = read_csv( _datasetFileName_csv )
  print_info( ">> dataset:", data_header, dataset )

  (cbook_header, codebook) = (list(), list())
  if( _codebookRandom ):
    codebook = [build_codebook_random( dataset ) for i in range(_dimCodebook)]
  else:
    (cbook_header, codebook) = read_csv( _codebookFileName_csv )
  print_info( ">> initial codebook:", cbook_header, codebook )

  # learn a codebook (given an initial one)
  ( codebook, totalError, errors ) = train_LVQ( dataset, codebook, _alpha, _maxEpoch )
  print_info( ">> learned codebook:", cbook_header, codebook,
              "totalError =", totalError )

  plot_error(errors)


#______________________________________________________________________________
# Exercise 5b: Impact of Number of Epochs on Final Error
def main_5b():
  print("\n" + "="*60)
  print("EXERCISE 5b: Impact of Number of Epochs")
  print("="*60)
  
  (data_header, dataset) = read_csv(_datasetFileName_csv)
  (cbook_header, codebook_initial) = read_csv(_codebookFileName_csv)
  
  epoch_values = []
  error_values = []
  
  print("\nRunning training with epochs from 1 to 100...")
  for max_epoch in range(1, 101):
    # Deep copy codebook to reset for each run
    codebook = [row[:] for row in codebook_initial]
    (_, totalError, _) = train_LVQ(dataset, codebook, 0.7, max_epoch)
    epoch_values.append(max_epoch)
    error_values.append(totalError)
    if max_epoch % 10 == 0:
      print(f"  MaxEpoch={max_epoch}, FinalError={totalError:.3f}")
  
  # Plot
  plt.figure(figsize=(10, 6))
  plt.plot(epoch_values, error_values, 'b-', linewidth=2)
  plt.xlabel("Maximum Epochs", fontsize=12)
  plt.ylabel("Final Total Error", fontsize=12)
  plt.title("Convergence Analysis: Total Error vs Number of Epochs\n(Fixed α=0.7, Non-random codebook)", fontsize=14)
  plt.grid(True, alpha=0.3)
  plt.savefig('plots/5b_epochs_vs_error.png', dpi=300, bbox_inches='tight')
  print(f"\n✓ Plot saved to: plots/5b_epochs_vs_error.png")
  plt.show()
  plt.close()


#______________________________________________________________________________
# Exercise 5c: Impact of Codebook Size
def main_5c():
  print("\n" + "="*60)
  print("EXERCISE 5c: Impact of Codebook Size")
  print("="*60)
  
  (data_header, dataset) = read_csv(_datasetFileName_csv)
  
  codebook_sizes = [2, 4, 6, 8, 10, 12, 15, 20, 25]
  avg_errors = []
  std_errors = []
  num_trials = 5
  
  print(f"\nTesting codebook sizes: {codebook_sizes}")
  print(f"Running {num_trials} trials per size for reliability...\n")
  
  for dim in codebook_sizes:
    errors_for_dim = []
    for trial in range(num_trials):
      seed(trial)
      codebook = [build_codebook_random(dataset) for i in range(dim)]
      (_, totalError, _) = train_LVQ(dataset, codebook, 0.7, 100)
      errors_for_dim.append(totalError)
    
    avg_error = sum(errors_for_dim) / len(errors_for_dim)
    std_error = (sum((e - avg_error)**2 for e in errors_for_dim) / len(errors_for_dim))**0.5
    avg_errors.append(avg_error)
    std_errors.append(std_error)
    print(f"  Codebook Size={dim:2d}: Avg Error={avg_error:.3f}, Std Dev={std_error:.3f}")
  
  # Plot
  plt.figure(figsize=(10, 6))
  plt.errorbar(codebook_sizes, avg_errors, yerr=std_errors, fmt='ro-', 
               linewidth=2, markersize=8, capsize=5, capthick=2, label='Avg Error ± Std')
  plt.xlabel("Codebook Size (Number of Vectors)", fontsize=12)
  plt.ylabel("Average Total Error (5 trials)", fontsize=12)
  plt.title("Impact of Codebook Size on Model Performance\n(α=0.7, 100 epochs, Random codebook)", fontsize=14)
  plt.grid(True, alpha=0.3)
  plt.legend()
  plt.savefig('plots/5c_codebook_size_vs_error.png', dpi=300, bbox_inches='tight')
  print(f"\n✓ Plot saved to: plots/5c_codebook_size_vs_error.png")
  plt.show()
  plt.close()


#______________________________________________________________________________
# Exercise 5d: Free Exploration - Learning Rate Impact
def main_5d():
  print("\n" + "="*60)
  print("EXERCISE 5d: Free Exploration - Learning Rate Impact")
  print("="*60)
  
  (data_header, dataset) = read_csv(_datasetFileName_csv)
  (cbook_header, codebook_initial) = read_csv(_codebookFileName_csv)
  
  alphas = [0.1, 0.3, 0.5, 0.7, 0.9]
  colors = ['blue', 'green', 'orange', 'red', 'purple']
  
  print(f"\nTesting learning rates: {alphas}")
  print("Training for 100 epochs each...\n")
  
  plt.figure(figsize=(12, 6))
  
  for alpha, color in zip(alphas, colors):
    codebook = [row[:] for row in codebook_initial]
    (_, totalError, errors) = train_LVQ(dataset, codebook, alpha, 100)
    plt.plot(range(len(errors)), errors, color=color, linewidth=2, 
             label=f'α={alpha}, Final Error={totalError:.3f}', alpha=0.8)
    print(f"  α={alpha}: Final Error={totalError:.3f}")
  
  plt.xlabel("Epoch", fontsize=12)
  plt.ylabel("Total Error", fontsize=12)
  plt.title("Learning Rate Comparison: Convergence Behavior\n(Non-random codebook, 100 epochs)", fontsize=14)
  plt.legend(loc='upper right')
  plt.grid(True, alpha=0.3)
  plt.savefig('plots/5d_learning_rate_comparison.png', dpi=300, bbox_inches='tight')
  print(f"\n✓ Plot saved to: plots/5d_learning_rate_comparison.png")
  plt.show()
  plt.close()


#______________________________________________________________________________
# Run all exercises
def run_all_exercises():
  print("\n" + "="*60)
  print("RUNNING ALL EXPERIMENTS FOR EXERCISE 5")
  print("="*60)
  
  main_5b()
  main_5c()
  main_5d()
  
  print("\n" + "="*60)
  print("✓ ALL EXPERIMENTS COMPLETED!")
  print("✓ All plots saved in 'plots/' directory")
  print("="*60 + "\n")


#______________________________________________________________________________
# The "main" of this module (is case this module is loaded from another module)
if __name__ == "__main__":
   # Uncomment the one you want to run:
   
   # main()              # Original: runs with current parameters
   # main_5b()           # Exercise 5b: Epochs vs Error
   # main_5c()           # Exercise 5c: Codebook Size vs Error
   # main_5d()           # Exercise 5d: Learning Rate Comparison
   run_all_exercises()   # Run all experiments for Exercise 5