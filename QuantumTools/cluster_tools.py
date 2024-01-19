import QuantumTools
import os
from typing import List

"""
 To use this in another script, import initialize_clusters and Cluster call directly
 initialize_clusters(calculation_method,run_directory,file_name)
 To use it as an script, the script create_run has been made, shich uses parser.
 To add a new cluster, just add one element to the cluster_name_list in 
 initialize_clusters function, the details of the cluster should be written in the
 library folder in a file called Name_of_cluster.cluster.
 To modify program versions just change qepath in the cluster object definition
 To add a new type of calculation just add a new function to the cluster class 
 If a new mode is added, remember to update the parser or create_run.py
"""

def initialize_clusters(calculation_method:str,run_directory:str,file_name:str,run_prefix:str,extra_info='')-> str: 
    QT_directory = QuantumTools.__file__.replace('__init__.py','')
    with open(QT_directory + 'Cluster.config','r') as f:
         cluster_name_list = f.read().replace('.cluster','').split()
    number_of_clusters = len(cluster_name_list)
    cluster_dict = dict.fromkeys(cluster_name_list)
    for i in cluster_name_list:
        cluster_dict[i] = Cluster(i)
        cluster_dict[i].run_prefix = run_prefix
        cluster_dict[i].extract_input_information() 
        if calculation_method == 'massive':
           cluster_dict[i].write_launcher(calculation_method,run_directory)
        else:
           cluster_dict[i].write_run(calculation_method,run_directory,file_name)
      
    return extra_info

class Cluster:
      def __init__(self,cluster_name:str):
         self.cluster_name: str = cluster_name
         self.qepath: str = ''
         self.wanpath: str = ''
         self.wtpath: str = ''
         self.header: str = ''
         self.run_prefix: str = ''
      def extract_input_information(self)-> None:
         QT_directory = QuantumTools.__file__.replace('__init__.py','')
         cluster_file = open(QT_directory + self.cluster_name + '.cluster','r')
         cluster_file_vector = cluster_file.readlines(); cluster_file.close() 
         cluster_header = '######### ' + self.cluster_name + ' run header #########\n'
         for line_number, line in enumerate(cluster_file_vector): 
             splitted_line = line.split(); splitted_line.append('')
             if splitted_line[0] == 'QE_dir:':
               self.qepath = splitted_line[1]
             if splitted_line[0] == 'Wan_dir:':
               self.wanpath = splitted_line[1]
             if splitted_line[0] == 'WT_dir:':
               self.wtpath = splitted_line[1]
             if line == cluster_header:
                header_starting_line = line_number
         for i in range(header_starting_line +1,len(cluster_file_vector),1):
             self.header =  self.header + cluster_file_vector[i]   
      def write_launcher(self,calculation_method:str,run_directory:str) -> None:
          run_name = self.cluster_name.lower() + '.serial.launcher.sh'
          run_file = open(os.path.join(run_directory,run_name), 'w' )
          run_file.write(self.header)
          run_file.write('\n')
      def write_run(self,calculation_method:str,run_directory:str,file_name:str) -> None:
          run_name = self.cluster_name.lower() + '.run_for_' + calculation_method.lower() + self.run_prefix + '.sh'
          run_file = open(os.path.join(run_directory,run_name), 'w' )
          run_file.write(self.header)
          run_file.write('\n')
          if calculation_method == 'basic_scf':
             self.write_basic_scf(file_name,run_file)  
          if calculation_method == 'spin_bands':
             self.write_spin_bands(file_name,run_file)
          if calculation_method == 'nospin_bands':
             self.write_nospin_bands(file_name,run_file)
          if calculation_method == 'projected':
             self.write_projected(file_name,run_file)
          if calculation_method == 'cd':
             self.write_cd_pp(file_name,run_file)
          if calculation_method == 'sd':
             self.write_sd_pp(file_name,run_file)
          if calculation_method == 'bader':
             self.write_bader_pp(file_name,run_file)
          if calculation_method == 'band_alignment':
             self.write_band_alignment(file_name,run_file)
          if calculation_method == 'spin_wannier':
             self.write_spin_wannier(file_name,run_file)
          if calculation_method == 'nospin_wannier':
             self.write_nospin_wannier(file_name,run_file)
          if calculation_method == 'force_theorem':
             self.write_force_theorem(file_name,run_file)
          if calculation_method == 'wt':
             self.write_wt('',run_file)
          run_file.close()
      def write_basic_scf(self,scf_input_name:str,run_file) -> None:  
          scf_output_name = scf_input_name.replace('.in','.out')
          run_file.write(\
          'srun ' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n') 
      def write_spin_bands(self,scf_input_name:str,run_file) -> None:  
          bands_input_name = scf_input_name.replace('scf','bands')
          bs1_input_name = scf_input_name.replace('scf','bs1')
          bs2_input_name = scf_input_name.replace('scf','bs2')
          scf_output_name = scf_input_name.replace('.in','.out')
          bands_output_name = bands_input_name.replace('.in','.out')
          bs1_output_name = bs1_input_name.replace('.in','.out')
          bs2_output_name = bs2_input_name.replace('.in','.out')
          run_file.write(\
          'srun ' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
          'srun ' + self.qepath + 'pw.x -i ' + bands_input_name + ' > ' + bands_output_name + '\n' + \
          'srun ' + self.qepath + 'bands.x -i ' + bs1_input_name + ' > ' + bs1_output_name + '\n' + \
          'srun ' + self.qepath + 'bands.x -i ' + bs2_input_name + ' > ' + bs2_output_name + '\n') 
      def write_nospin_bands(self,scf_input_name:str,run_file) -> None:  
          bands_input_name = scf_input_name.replace('scf','bands')
          bs_input_name = scf_input_name.replace('scf','bs')
          scf_output_name = scf_input_name.replace('.in','.out')
          bands_output_name = bands_input_name.replace('.in','.out')
          bs_output_name = bs_input_name.replace('.in','.out')
          run_file.write(\
          'srun ' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
          'srun ' + self.qepath + 'pw.x -i ' + bands_input_name + ' > ' + bands_output_name + '\n' + \
          'srun ' + self.qepath + 'bands.x -i ' + bs_input_name + ' > ' + bs_output_name + '\n') 
      def write_projected(self,scf_input_name:str,run_file) -> None:  
          nscf_input_name = scf_input_name.replace('scf','nscf')
          proj_input_name = scf_input_name.replace('scf','proj')
          scf_output_name = scf_input_name.replace('.in','.out')
          nscf_output_name = nscf_input_name.replace('.in','.out')
          proj_output_name = proj_input_name.replace('.in','.out')
          run_file.write(\
          'srun ' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
          'srun ' + self.qepath + 'pw.x -i ' + nscf_input_name + ' > ' + nscf_output_name + '\n' + \
          'srun ' + self.qepath + 'projwfc.x -i ' + proj_input_name + ' > ' + proj_output_name + '\n') 
      def write_cd_pp(self,scf_input_name:str,run_file) -> None:  
          pp_input_name = scf_input_name.replace('scf','cd.pp')
          scf_output_name = scf_input_name.replace('.in','.out')
          pp_output_name = pp_input_name.replace('.in','.out')
          run_file.write(\
          'srun ' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
          'srun ' + self.qepath + 'pp.x -i ' + pp_input_name + ' > ' + pp_output_name + '\n') 
      def write_sd_pp(self,scf_input_name:str,run_file) -> None:  
          pp_input_name = scf_input_name.replace('scf','sd.pp')
          scf_output_name = scf_input_name.replace('.in','.out')
          pp_output_name = pp_input_name.replace('.in','.out')
          run_file.write(\
          'srun ' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
          'srun ' + self.qepath + 'pp.x -i ' + pp_input_name + ' > ' + pp_output_name + '\n') 
      def write_bader_pp(self,scf_input_name:str,run_file) -> None: 
          all_input_name = scf_input_name.replace('scf','all.pp')
          valence_input_name = scf_input_name.replace('scf','valence.pp')
          scf_output_name = scf_input_name.replace('.in','.out')
          all_output_name = all_input_name.replace('.in','.out')
          valence_output_name = valence_input_name.replace('.in','.out')
          valence_cube = valence_input_name.replace('.pp.in','.cube')
          all_cube = all_input_name.replace('.pp.in','.cube')
          run_file.write(\
          'srun ' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
          'srun ' + self.qepath + 'pp.x -i ' + all_input_name + ' > ' + all_output_name + '\n' + \
          'srun ' + self.qepath + 'pp.x -i ' + valence_input_name + ' > ' + valence_output_name + '\n' + \
          'bader ' + valence_cube + ' -ref ' + all_cube ) 
      def write_band_alignment(self,scf_input_name:str,run_file) -> None: 
          pp_input_name = scf_input_name.replace('scf','wf.pp')
          avg_input_name = scf_input_name.replace('scf','avg')
          scf_output_name = scf_input_name.replace('.in','.out')
          pp_output_name = pp_input_name.replace('.in','.out')
          avg_output_name = avg_input_name.replace('.in','.out')
          run_file.write(\
          'srun ' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
          'srun ' + self.qepath + 'pp.x -i ' + pp_input_name + ' > ' + pp_output_name + '\n' + \
          'mpirun -np 1 ' + self.qepath + 'average.x ' + '<' + avg_input_name + ' > ' + avg_output_name + '\n') 
      def write_spin_wannier(self,scf_input_name:str,run_file) -> None:  
          nscf_input_name = scf_input_name.replace('scf','nscf')
          pw2wan_up_input_name = scf_input_name.replace('scf','up.pw2wan')
          pw2wan_down_input_name = scf_input_name.replace('scf','down.pw2wan')
          win_up_input_name = scf_input_name.replace('scf.in','up.win')
          win_down_input_name = scf_input_name.replace('scf.in','down.win')
          scf_output_name = scf_input_name.replace('.in','.out')
          nscf_output_name = nscf_input_name.replace('.in','.out')
          pw2wan_up_output_name = pw2wan_up_input_name.replace('.in','.out')
          pw2wan_down_output_name = pw2wan_down_input_name.replace('.in','.out')
          run_file.write(\
          'srun ' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
          'srun ' + self.qepath + 'pw.x -i ' + nscf_input_name + ' > ' + nscf_output_name + '\n' + \
          'srun ' + self.wanpath + 'wannier90.x -pp ' + win_up_input_name + '\n' + \
          'srun ' + self.qepath + 'pw2wannier90.x -i ' + pw2wan_up_input_name + ' > ' + pw2wan_up_output_name + '\n' + \
          'srun ' + self.wanpath + 'wannier90.x ' + win_up_input_name + '\n' + \
          'srun ' + self.wanpath + 'wannier90.x -pp ' + win_down_input_name + '\n' + \
          'srun ' + self.qepath + 'pw2wannier90.x -i ' + pw2wan_down_input_name + ' > ' + pw2wan_down_output_name + '\n' + \
          'srun ' + self.wanpath + 'wannier90.x ' + win_down_input_name + '\n') 
      def write_nospin_wannier(self,scf_input_name:str,run_file) -> None:
          nscf_input_name = scf_input_name.replace('scf','nscf')
          pw2wan_input_name = scf_input_name.replace('scf','pw2wan')
          win_input_name = scf_input_name.replace('scf.in','win')
          scf_output_name = scf_input_name.replace('.in','.out')
          nscf_output_name = nscf_input_name.replace('.in','.out')
          pw2wan_output_name = pw2wan_input_name.replace('.in','.out')
          run_file.write(\
          'srun ' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
          'srun ' + self.qepath + 'pw.x -i ' + nscf_input_name + ' > ' + nscf_output_name + '\n' + \
          'srun ' + self.wanpath + 'wannier90.x -pp ' + win_input_name + '\n' + \
          'srun ' + self.qepath + 'pw2wannier90.x -i ' + pw2wan_input_name + ' > ' + pw2wan_output_name + '\n' + \
          'srun ' + self.wanpath + 'wannier90.x ' + win_input_name + '\n') 
      def write_force_theorem(self,scf_input_name:str,run_file) -> None:  
          x_nscf_input_name = scf_input_name.replace('scf','x.nscf')
          y_nscf_input_name = scf_input_name.replace('scf','y.nscf')
          z_nscf_input_name = scf_input_name.replace('scf','z.nscf')
          scf_output_name = scf_input_name.replace('.in','.out')
          x_nscf_output_name = x_nscf_input_name.replace('.in','.out')
          y_nscf_output_name = y_nscf_input_name.replace('.in','.out')
          z_nscf_output_name = z_nscf_input_name.replace('.in','.out')
          run_file.write(\
          'srun ' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
          'cp -r tmp tmp_x\n' + 'cp -r tmp tmp_y\n' +  'cp -r tmp tmp_z\n' + \
          'srun ' + self.qepath + 'pw.x -i ' + x_nscf_input_name + ' > ' + x_nscf_output_name + '\n' + \
          'srun ' + self.qepath + 'pw.x -i ' + y_nscf_input_name + ' > ' + y_nscf_output_name + '\n' + \
          'srun ' + self.qepath + 'pw.x -i ' + z_nscf_input_name + ' > ' + z_nscf_output_name + '\n') 
      def write_wt(self,scf_input_name:str,run_file) -> None:  
          run_file.write(\
          'srun ' + self.wtpath +  ' wt.x wt.in\n'
          )
