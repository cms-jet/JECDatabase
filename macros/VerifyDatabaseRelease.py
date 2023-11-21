from utils import *

class CorrectionInfoBase():
    def __init__(self):
        self.algos = ['PFchs', 'PFPuppi']
        # self.algos = ['PFchs']
        # self.algos = ['PFPuppi']
        self.radii = ['AK4', 'AK8']
        # self.radii = ['AK4']
        # self.radii = ['AK8']
        self.levels = [ 'L1FastJet', 'L2Relative', 'L3Absolute', 'L1RC', 'DataMcSF_L1RC', 'L2Residual', 'L2L3Residual', 'Uncertainty', 'UncertaintySources']
        # self.levels = [ 'L1FastJet', 'L1RC', 'DataMcSF_L1RC']
        # self.levels = [ 'L1FastJet', 'L2Relative', 'L3Absolute', 'L1RC', 'DataMcSF_L1RC']
        # self.levels = [ 'L1FastJet', 'L2Relative', 'L3Absolute']
        # self.levels = [ 'L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']
        self.levels_JER = ['SF', 'PtResolution', 'EtaResolution', 'PhiResolution']
        self.runs = {'UL16APV': ['BCDEF'],
                     'UL16': ['FGH'],
                     'UL17': ['B', 'C', 'D', 'E', 'F', 'H'],
                     'UL18': ['A', 'B', 'C', 'D'],
                     # 'Run3': ['A', 'B', 'C', 'D',]
                     'Run3': ['C','D'],
                     'Prompt22': ['F', 'G'],
                     'Prompt23': ['C'],
                     }
    
    def isAk8chs(self, algo, radius):
        if 'chs' in algo.lower() and '8' in radius: return True
        return False


class RepositoryInfo(CorrectionInfoBase):
    def __init__(self, tag, year, version, repo='JECDatabase'):
        CorrectionInfoBase.__init__(self)
        self.tag = tag
        self.year = year
        self.version = version
        self.repo = repo
        self.isJRDatabase = self.repo == 'JRDatabase'
        if self.isJRDatabase:
            self.tag = self.tag
            self.levels = self.levels_JER
            for year in self.runs.keys():
                self.runs[year] = ['']

    def getFolderPath(self, folder, basefolder = os.getcwd()):
        ''' Returns the absolute path of a given folder inside the textFiles directory. Recursive function. '''
        basefolder = basefolder.replace('JECDatabase',self.repo)
        if os.path.exists(os.path.join(basefolder,'textFiles')):
            return os.path.join(basefolder,'textFiles', folder)
        else:
            return self.getFolderPath(folder, basefolder = basefolder.strip(basefolder.split('/')[-1]))

    def getFilePath(self, folder,filename):
        ''' Returns the absolute path of a given file inside the folder. '''
        return os.path.join(self.getFolderPath(folder), self.getFolderPath(folder).split('/')[-1]+filename)

    def getFilePostfix(self, level, radius, algo):
        ''' Returns the postfix for a given correction. '''
        return '_'+level+'_'+radius+algo+'.txt'

    def getListofFolders(self):
        ''' Returns the list of MC and Data folders for a given version. '''
        folders = [self.getFolderPath(self.tag+self.year+'_'+self.version+'_MC')]
        for run in self.runs[self.year]:
            folder = self.getFolderPath(self.tag+self.year+'_Run'+run+'_'+self.version+'_DATA')
            if self.isJRDatabase: folder = folder.replace('_Run','')
            folders.append(folder)
        return folders




class RepositoryChecker(RepositoryInfo):
    def __init__(self, tag, year, version, repo):
        RepositoryInfo.__init__(self, tag, year, version, repo)
        self.corrections = {'copy from MC':['L2Relative']}
        if self.isJRDatabase:
            self.corrections = {'copy from MC':['PtResolution', 'EtaResolution', 'PhiResolution']}

    def L3AbsoluteDummy(self):
        lines = ['{1         JetEta         1     JetPt          1     Correction     L3Absolute}']
        lines.append('-5.191          5.191     2         1      10000')
        return lines

    def L1FastJetPuppiDummy(self):
        lines = ['{1         JetEta         3     Rho     JetPt     JetA          1     Correction     L1FastJet}']
        lines.append('-5.191          5.191     6         0       200        10      3000          0        10')
        return lines

    def JERSFDummy(self):
        lines = ['{1         JetEta         0     None    ScaleFactor}']
        lines.append('-50             50        3         1       1       1')
        return lines

    def L2L3ResDummy(self):
        lines = ['{1         JetEta         1     JetPt          1     Correction     L2Relative}']
        lines.append('-5.191          5.191     2         4      5000')
        return lines

    def createNewFolder(self):
        for folder in self.getListofFolders():
            if os.path.exists(folder):
                print(yellow('This directory already exists: '+folder+'. No folder created.'))
            else:
                print(green('Creating directory: '+folder))
                os.makedirs(folder)

    def writeLinesToFile(self, lines, filename):
        with open(filename, 'w') as f:
            for l in lines:
                f.write(l+'\n')

    def createDummies(self):
        ''' Create dummy files for relevant corrections. '''
        for folder in self.getListofFolders():
            for algo in self.algos:
                for radius in self.radii:
                    if self.isAk8chs(algo, radius): continue
                    if self.isJRDatabase:
                        if 'DATA' in folder:
                            filename = self.getFilePath(folder, self.getFilePostfix('SF', radius, algo))
                            self.writeLinesToFile(self.JERSFDummy(), filename)
                    else:
                        filename = self.getFilePath(folder, self.getFilePostfix('L3Absolute', radius, algo))
                        self.writeLinesToFile(self.L3AbsoluteDummy(), filename)
                        if 'PFPuppi' in algo:
                            filename = self.getFilePath(folder, self.getFilePostfix('L1FastJet', radius, algo))
                            self.writeLinesToFile(self.L1FastJetPuppiDummy(), filename)
                        if 'MC' in folder:
                            filename = self.getFilePath(folder, self.getFilePostfix('L2Residual', radius, algo))
                            self.writeLinesToFile(self.L2L3ResDummy(), filename)
                            filename = self.getFilePath(folder, self.getFilePostfix('L2L3Residual', radius, algo))
                            self.writeLinesToFile(self.L2L3ResDummy(), filename)

    def cloneMCToData(self):
        ''' Clone files from MC to Data for relevant corrections.
            Assumes that the first element of getListofFolders is MC and the rest is Data.
        '''
        folders = self.getListofFolders()
        if self.isJRDatabase:
            basefolder = os.getcwd().replace('JECDatabase',self.repo)
            filepath = os.path.join(basefolder[:basefolder.find(self.repo)+len(self.repo)],'scripts')
            outputfilename = 'JERMultiplier'
            if (not os.path.exists(os.path.join(filepath,outputfilename))):
                print(yellow(outputfilename+' does not exist. Creating executable.'))
                os.system('g++ '+filepath+'/MultiplyTextFiles.cpp -o '+filepath+'/'+outputfilename)
        for algo in self.algos:
            for radius in self.radii:
                if self.isAk8chs(algo, radius): continue
                for level in self.corrections['copy from MC']:
                    basename = self.getFilePostfix(level, radius, algo)
                    input = self.getFilePath(folders[0], basename)
                    if (not os.path.exists(input)):
                        print(red(input+' does not exist. Interrupting copy.'))
                        return
                    for folder in folders[1:]:
                        output = self.getFilePath(folder, basename)
                        if (os.path.exists(output) and not self.isJRDatabase):
                            print(yellow(output+' already exist. Skipping copy.'))
                        else:
                            if self.isJRDatabase:
                                sf_file = input.replace(level,'SF')
                                if (not os.path.exists(sf_file)):
                                    print(red(sf_file+' does not exist. Interrupting copy.'))
                                    return
                                os.system(filepath+'/'+outputfilename+' --JERFileName '+input+' --JERSFFileName '+sf_file+' --Output '+output)
                            else:
                                shutil.copy(input, output)

    def diffFiles(self, file1, file2, expected_difference=True):
        ''' Check if 2 files if two files are different. '''
        skip = False
        if (not os.path.exists(file1)):
            print(red(file1+' does not exist. Interrupting diff.'))
            skip = True
        if (not os.path.exists(file2)):
            print(red(file2+' does not exist. Interrupting diff.'))
            skip = True
        if skip: return
        lines1 = open(file1).readlines()
        lines2 = open(file2).readlines()
        is_different = len(list(set(lines1)-set(lines2)))!=0
        if expected_difference and not is_different:
            print(blue('Performing check on: '+file1+' '+file2))
            print(yellow('  --> Files are identical while they should be different.'))
        if not expected_difference and is_different:
            print(blue('Performing check on: '+file1+' '+file2))
            print(yellow('  --> Files differ while they should be identical.'))

    def diffFolders(self, folder1, folder2):
        ''' Run iteratively diffFiles for all files in the given folders. '''
        for algo in self.algos:
            for radius in self.radii:
                if self.isAk8chs(algo, radius): continue
                for level in self.levels:
                    if 'DataMcSF_L1RC' in level and ('MC' in folder1 or 'MC' in folder2): continue
                    if 'L1RC' in level and 'PFPuppi' in algo: continue
                    basename = self.getFilePostfix(level, radius, algo)
                    self.diffFiles(self.getFilePath(folder1,basename),self.getFilePath(folder2,basename))

    def verifyFolderContent(self):
        ''' Check if all expected files are in the given folder. '''
        folders = self.getListofFolders()
        for folder in folders:
            for algo in self.algos:
                for radius in self.radii:
                    if self.isAk8chs(algo, radius): continue
                    for level in self.levels:
                        if 'DataMcSF_L1RC' in level and 'MC' in folder: continue
                        if 'L1RC' in level and 'PFPuppi' in algo: continue
                        fname = self.getFilePath(folder, self.getFilePostfix(level, radius, algo))
                        if (not os.path.exists(fname)):
                            print(red(fname+' does not exist.'))
                            continue
                        if self.isJRDatabase:
                            pass
                        else:
                            if folder!=folders[0]:
                                if 'DataMcSF_L1RC' in level: continue
                                runName = list(filter(lambda x: x.startswith('Run'), fname.split('/')[-1].split('_')))[0]
                                if level in self.corrections['copy from MC'] or 'L3Absolute' in level or ('L1FastJet' in level and 'PFPuppi' in algo) or ('Uncertainty' in level):
                                    self.diffFiles(fname, fname.replace('DATA','MC').replace(runName+'_',''), expected_difference=False)
                                else:
                                    self.diffFiles(fname, fname.replace('DATA','MC').replace(runName+'_',''), expected_difference=True)

    def CreateTarball(self):
        for folder in self.getListofFolders():
            base_folder = folder[:folder.find('textFiles')]
            txt_folder = folder[folder.find('textFiles'):]
            command =  'cd '+base_folder
            command += '; ./scripts/createTarball.sh ' + txt_folder
            command += '; mv '+folder+'/'+folder.split('/')[-1]+'.tar.gz '+base_folder+'/tarballs'
            os.system(command)
    
    def CreateDatabase(self):
        return
        for folder in self.getListofFolders():
            base_folder = folder[:folder.find('textFiles')]
            txt_folder = folder[folder.find('textFiles'):]
            era = txt_folder.split('/')[1]
            command =  'cd '+base_folder
            command += '; cmsRun '+base_folder+'scripts/createDBFromTxtFiles.py era='+era+' path='+txt_folder+' &> "'+era+'.log"'
            # command += '; mv '+folder+'/'+folder.split('/')[-1]+'.tar.gz '+base_folder+'/tarballs'
            print(command)
            # os.system(command)





#this class should verify if the JECs can be read
class JECsChecker(RepositoryInfo):
    def __init__(self, tag, year, version, repo):
        RepositoryInfo.__init__(self, tag, year, version, repo)
        self.etas = [0, 1.3, 2.5, 3.0, 5.0, 6.0]
        self.pts = [15, 30, 90, 300, 1000, 3000]
        self.rhos = [0, 5, 10, 15, 20, 25, 30, 40, 50]
        self.rhos = [0, 15, 30]

    def verifyJECs(self):
        ''' A crash is expected if the files are not read properly. '''
        import ROOT as rt
        if self.isJRDatabase:
            rt.gInterpreter.ProcessLine('#include "JetMETCorrections/Modules/interface/JetResolution.h"')
        else:
            ''' Produce an annoying warning which cannot be easily masked. '''
            #include "JetMETCorrections/JetCorrector/interface/JetCorrector.h"
            rt.gInterpreter.ProcessLine('#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"')
            rt.gInterpreter.ProcessLine('#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"')

        for folder in self.getListofFolders():
            for algo in self.algos:
                for radius in self.radii:
                    if self.isAk8chs(algo, radius): continue
                    area = rt.TMath.Pi()*(0.4*0.4 if '4' in radius else 0.8*0.8)
                    if self.isJRDatabase:
                        print('checking')
                        for level in self.levels:
                            fname = self.getFilePath(folder, self.getFilePostfix(level, radius, algo))
                            if not os.path.exists(fname):
                                print(yellow('This file doesn\'t exists: '+fname))
                                continue
                            print(fname)
                            if 'SF' in level:
                                JER_sf = rt.JME.JetResolutionScaleFactor(fname)
                            else:
                                JER = rt.JME.JetResolution(fname)
                            for eta in self.etas:
                                for pt in self.pts:
                                    for rho in self.rhos:
                                        pars = rt.JME.JetParameters().setJetPt(pt).setJetEta(eta).setRho(rho)
                                        if 'SF' in level:
                                            sf = JER_sf.getScaleFactor(pars)
                                            # print(eta,pt,rho,round(sf,3))
                                        else:
                                            jer = JER.getResolution(pars)
                                            # print(eta,pt,rho,round(jer,3))
                    else:
                        params = rt.vector('JetCorrectorParameters')()
                        for level in self.levels:
                            if 'Uncertainty' in level: continue
                            if 'DataMcSF' in level: continue
                            if 'L1' in level and 'Puppi' in algo: continue
                            # if 'L1RC' in level:
                            #     print(red('This is to be fixed: L1RC'))
                            #     continue
                            if 'RunH' in folder:
                                print(red('This is to be fixed: RunH'))
                                continue
                            fname = self.getFilePath(folder, self.getFilePostfix(level, radius, algo))
                            if not os.path.exists(fname):
                                print(red('This is to be fixed: missin file. '+fname))
                                continue
                            else: params.push_back(rt.JetCorrectorParameters(fname))
                        if params.size()==0:
                            print(red('Is this really expected? '+folder+' '+algo+' '+radius))
                            continue
                        JEC = rt.FactorizedJetCorrector(params)
                        for eta in self.etas:
                            for pt in self.pts:
                                for rho in self.rhos:
                                    JEC.setJetEta(eta)
                                    JEC.setJetPt(pt)
                                    JEC.setRho(rho)
                                    JEC.setJetA(area)
                                    jec = JEC.getCorrection()
                                    # print(eta,pt,rho,round(jec,3))



def VerifyDatabaseRelease():
    repo = 'JECDatabase'
    repo = 'JRDatabase'

    years = {
        'JECDatabase': {'UL16APV':'V2','UL16':'V2','UL17':'V2','UL18':'V2'},
        'JRDatabase':  {'UL16APV':'JRV4','UL16':'JRV4','UL17':'JRV1','UL18':'JRV1'},
             }
    years = {
        # 'JECDatabase': {'Prompt22':'V1'},
        # 'JRDatabase':  {'Prompt23':'JRV2'},
        # 'JRDatabase':  {'Prompt22':'JRV1'},
             }
    tag = 'Summer20'
    tag = 'Winter23'
    tag = 'Summer22EE'
    for year,version in years[repo].items():
        RC = RepositoryChecker(tag=tag, year=year, version=version, repo=repo)
        # RC.createNewFolder()
        # RC.createDummies()
        # RC.cloneMCToData()
        # RC.verifyFolderContent()
        # RC.CreateTarball()
        # RC.CreateDatabase()
        JC = JECsChecker(tag=tag, year=year, version=version, repo=repo)
        # JC.verifyJECs()



def main():
    VerifyDatabaseRelease()

if __name__ == '__main__':
    main()
