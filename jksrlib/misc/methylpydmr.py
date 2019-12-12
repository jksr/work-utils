import pandas as pd

class MethylPyDMR:
    
    def __init__(self, dmrfn):
        self.df = pd.read_csv(dmrfn, sep='\t')
        self.bed3 = self.df[self.df.columns[:3]]
        self.head = self.df[self.df.columns[:4]]
        self.samples = self.df.columns[ self.df.columns.str.startswith('methylation_level_') ]\
                            .str.replace('methylation_level_','').to_list()
        self.methyl_level_df = None
        self.methyl_level_df = self._methlv()
        self.hyp_df = None
        self.hyp_df = self._hyp()
        
    def _methlv(self):
        if self.methyl_level_df is None:
            methlv = self.df[ self.df.columns[self.df.columns.str.startswith('methylation_level_')] ]
            methlv.columns = self.samples
            self.methyl_level_df = pd.concat([self.head, methlv], axis=1)
        return self.methyl_level_df
    
    def _hyp(self):
        if self.hyp_df is None:
            hypdict = {}
            for sam in self.samples:
                hypdict[sam] = self.df['hypermethylated_samples'].str.split(',').apply(
                                                        lambda x: 1 if isinstance(x,list) and sam in x else 0)
            hyper = pd.DataFrame.from_dict(hypdict)
            for sam in self.samples:
                hypdict[sam] = self.df['hypomethylated_samples'].str.split(',').apply(
                                                        lambda x: 1 if isinstance(x,list) and sam in x else 0)
            hypo = pd.DataFrame.from_dict(hypdict)
            self.hyp_df = pd.concat([self.head,hyper-hypo], axis=1)
        return self.hyp_df
#         hyp = self.df[self.df.columns.str.endswith('methylated_samples')]

    def hypo_bed(self, sample):
        return self.bed3[self.hyp_df[sample]<0]

    def hyper_bed(self, sample):
        return self.bed3[self.hyp_df[sample]>0]
