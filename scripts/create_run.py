# TO DO LIST
"""
-name run
-update runs

"""

#Instructions

"""
 to use this, import this file and call the class function of your calculation
 type, for example write_wannier(files....)
 to add a new cluster, just define the new cluster object
 to modify program versions just change qepath in the cluster object definition
 to add a new type of calculation just add a new function to the cluster class 
"""

# Examples of usage
"""
raven.write_nospin_wannier('feps3.z.scf.in')
cobra.write_nospin_wannier('feps3.z.scf.in')
tirant.write_nospin_wannier('feps3.z.scf.in')
"""

class cluster:
    def __init__(self,qepath,wanpath,heading,file_name):
        self.qepath = qepath
        self.wanpath = wanpath
        self.heading = heading
        self.file_name = file_name
        self.opened_file = open(self.file_name, 'w')
    def write_heading(self):
        self.opened_file.write(self.heading)
    def write_spin_bands(self,scf_input_name):  
        bands_input_name = scf_input_name.replace('scf','bands')
        bs1_input_name = scf_input_name.replace('scf','bs1')
        bs2_input_name = scf_input_name.replace('scf','bs2')
        scf_output_name = scf_input_name.replace('.in','.out')
        bands_output_name = bands_input_name.replace('.in','.out')
        bs1_output_name = bs1_input_name.replace('.in','.out')
        bs2_output_name = bs2_input_name.replace('.in','.out')
        self.write_heading() 
        self.opened_file.write(\
        'srun' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
        'srun' + self.qepath + 'pw.x -i ' + bands_input_name + ' > ' + bands_output_name + '\n' + \
        'srun' + self.qepath + 'bands.x -i ' + bs1_input_name + ' > ' + bs1_output_name + '\n' + \
        'srun' + self.qepath + 'bands.x -i ' + bs2_input_name + ' > ' + bs2_output_name + '\n') 
    def write_nospin_bands(self,scf_input_name):  
        bands_input_name = scf_input_name.replace('scf','bands')
        bs_input_name = scf_input_name.replace('scf','bs')
        scf_output_name = scf_input_name.replace('.in','.out')
        bands_output_name = bands_input_name.replace('.in','.out')
        bs_output_name = bs_input_name.replace('.in','.out')
        self.write_heading() 
        self.opened_file.write(\
        'srun' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
        'srun' + self.qepath + 'pw.x -i ' + bands_input_name + ' > ' + bands_output_name + '\n' + \
        'srun' + self.qepath + 'bands.x -i ' + bs_input_name + ' > ' + bs_output_name + '\n') 
    def write_projected(self,scf_input_name):  
        nscf_input_name = scf_input_name.replace('scf','nscf')
        proj_input_name = scf_input_name.replace('scf','proj')
        scf_output_name = scf_input_name.replace('.in','.out')
        nscf_output_name = nscf_input_name.replace('.in','.out')
        proj_output_name = proj_input_name.replace('.in','.out')
        self.write_heading() 
        self.opened_file.write(\
        'srun' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
        'srun' + self.qepath + 'pw.x -i ' + nscf_input_name + ' > ' + nscf_output_name + '\n' + \
        'srun' + self.qepath + 'projwfc.x -i ' + proj_input_name + ' > ' + proj_output_name + '\n') 
    def write_pp(self,scf_input_name):  
        pp_input_name = scf_input_name.replace('scf','pp')
        scf_output_name = scf_input_name.replace('.in','.out')
        pp_output_name = pp_input_name.replace('.in','.out')
        self.write_heading() 
        self.opened_file.write(\
        'srun' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
        'srun' + self.qepath + 'pp.x -i ' + pp_input_name + ' > ' + pp_output_name + '\n') 
    def write_spin_wannier(self,scf_input_name):  
        nscf_input_name = scf_input_name.replace('scf','nscf')
        pw2wan_up_input_name = scf_input_name.replace('scf','up.pw2wan')
        pw2wan_down_input_name = scf_input_name.replace('scf','down.pw2wan')
        win_up_input_name = scf_input_name.replace('scf.in','up.win')
        win_down_input_name = scf_input_name.replace('scf.in','down.win')
        scf_output_name = scf_input_name.replace('.in','.out')
        nscf_output_name = nscf_input_name.replace('.in','.out')
        pw2wan_up_output_name = pw2wan_up_input_name.replace('.in','.out')
        pw2wan_down_output_name = pw2wan_down_input_name.replace('.in','.out')
        self.write_heading() 
        self.opened_file.write(\
        'srun' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
        'srun' + self.qepath + 'pw.x -i ' + nscf_input_name + ' > ' + nscf_output_name + '\n' + \
        'srun' + self.wanpath + 'wannier90.x -pp ' + win_up_input_name + '\n' + \
        'srun' + self.qepath + 'pw2wan.x -i ' + pw2wan_up_input_name + ' > ' + pw2wan_up_output_name + '\n' + \
        'srun' + self.wanpath + 'wannier90.x ' + win_up_input_name + '\n' + \
        'srun' + self.wanpath + 'wannier90.x -pp ' + win_down_input_name + '\n' + \
        'srun' + self.qepath + 'pw2wan.x -i ' + pw2wan_down_input_name + ' > ' + pw2wan_down_output_name + '\n' + \
        'srun' + self.wanpath + 'wannier90.x ' + win_down_input_name + '\n') 
    def write_nospin_wannier(self,scf_input_name):
        nscf_input_name = scf_input_name.replace('scf','nscf')
        pw2wan_input_name = scf_input_name.replace('scf','pw2wan')
        win_input_name = scf_input_name.replace('scf.in','win')
        scf_output_name = scf_input_name.replace('.in','.out')
        nscf_output_name = nscf_input_name.replace('.in','.out')
        pw2wan_output_name = pw2wan_input_name.replace('.in','.out')
        self.write_heading() 
        self.opened_file.write(\
        'srun' + self.qepath + 'pw.x -i ' + scf_input_name + ' > ' + scf_output_name + '\n' + \
        'srun' + self.qepath + 'pw.x -i ' + nscf_input_name + ' > ' + nscf_output_name + '\n' + \
        'srun' + self.wanpath + 'wannier90.x -pp ' + win_input_name + '\n' + \
        'srun' + self.qepath + 'pw2wan.x -i ' + pw2wan_input_name + ' > ' + pw2wan_output_name + '\n' + \
        'srun' + self.wanpath + 'wannier90.x ' + win_input_name + '\n') 
tirant = cluster(\
' ',\
' ',\
'#!/bin/bash -l\n' + \
'#SBATCH --job-name=job_name\n' + \
'#SBATCH --nodes=6\n' + \
'#SBATCH --workdir=.\n' + \
'#SBATCH --output=task_%j.out\n' + \
'#SBATCH --error=task_%j.err\n' + \
'#SBATCH --ntasks=16\n' + \
'#SBATCH --cpus-per-task=2\n' + \
'#SBATCH --tasks-per-node=8\n' + \
'#SBATCH --time=0-00:30:00\n' + \
'export LD_LIBRARY_PATH=/storage/apps/Intel_Comp/xe_2019u4/compilers_and' + \
'_libraries_2019.4.243/linux/mpi/intel64/lib/:$LD_LIBRARY_PATH\n' + \
'module load intel/2019.4.243\n' + \
'module load mkl/2019.4.243\n' + \
'module load impi/2019.4.243\n' + \
'module load qe/6.5.0\n' + \
'module load wannier90/3.1\n' + \
'ulimit -s unlimited\n', \
'tirant.run.sh')
raven = cluster(\
' ',\
' ',\
'#!/bin/bash -l\n' + \
'#SBATCH -o ./task.out.%j\n' + \
'#SBATCH -e ./task.err.%j\n' + \
'#SBATCH -D ./\n' + \
'#SBATCH -J job_name\n' + \
'#SBATCH --nodes=1\n' + \
'#SBATCH --ntasks-per-node=72\n' + \
'#SBATCH --partition=general\n' + \
'#SBATCH --time=06:00:00\n' + \
'module load intel/19.1.2\n' + \
'module load impi/2019.8\n' + \
'module load qe/6.8\n' + \
'module load wannier90/3.1.0\n' + \
'ulimit -s unlimited\n' + \
'export LD_LIBRARY_PATH=/mpcdf/soft/SLE_12_SP3/packages/x86_64/' + \
'intel_parallel_studio/2018.3/mkl/lib/intel64:/raven/u/system/soft/SLE_15/' + \
'packages/x86_64/anaconda/3/2020.02/lib:$LD_LIBRARY_PATH\n', \
'raven.run.sh')
cobra = cluster(\
'/u/jojaibal/qe-6.8/bin/',\
'/u/jojaibal/wannier90-3.1.0/',\
'#!/bin/bash -l\n' + \
'#SBATCH --nodes=2\n' + \
'#SBATCH --ntasks-per-node=40\n' + \
'#SBATCH --time 0-09:30:00\n' + \
'#SBATCH --partition=medium\n' + \
'#SBATCH --job-name= job_name\n' + \
'#SBATCH --output=task.out.%j\n' + \
'#SBATCH --error=task.err.%j\n' + \
'#SBATCH --exclusive\n' + \
'ulimit -s unlimited\n' + \
'export LD_LIBRARY_PATH=/mpcdf/soft/SLE_12_SP3/packages/x86_64/' + \
'intel_parallel_studio/2018.3/mkl/lib/intel64:$LD_LIBRARY_PATH\n' + \
'module load intel/19.1.3\n' + \
'module load mkl/2020.4\n' + \
'module load parallel/201807\n' + \
'module load impi/2019.9\n', \
'cobra.run.sh')











