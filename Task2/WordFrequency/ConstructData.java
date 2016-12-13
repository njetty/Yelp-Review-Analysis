import org.apache.lucene.document.Document;
import org.apache.lucene.index.*;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.BytesRef;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

/**
 * Created by sujith on 12/4/2016.
 */
public class ConstructData {
    public class Data{
        private String Review_id;
        private List<Integer> feats;
        private int Label;
        public Data(String id,List<Integer> f,int rating){
            this.Review_id=id;
            this.Label=rating;
            this.feats=f;
        }
    }
    public int termfreq(String s,LeafReaderContext leaf ,int startdoc,int docNum) throws IOException{
        PostingsEnum de= MultiFields.getTermDocsEnum(leaf.reader(), "TEXT", new BytesRef(s));
        int doc;
        if(de!=null){
            while((doc=de.nextDoc())!=PostingsEnum.NO_MORE_DOCS){
                if(de.docID()+startdoc==docNum)
                        return de.freq();
                }
            }
            return 0;
        }
    public void constructData(List<String> features) throws IOException {
        String csvFile = "C:\\Users\\sujit\\Documents\\SearchDataset\\YelpReview.csv";
        FileWriter writer = new FileWriter(csvFile);

        String indexPath = "C:\\Users\\sujit\\Documents\\SearchDataset\\indexPath1L";
        IndexReader reader= DirectoryReader.open(FSDirectory.open(Paths.get(indexPath)));
        System.out.println("Total Documents"+reader.numDocs());
        //Writing Column Names for the CSV
        String COMMA=",";
        String NEWLINE="\n";
        String ColNames="";
        writer.append("REVIEW_ID");
        writer.append(COMMA);
        for(String s:features){
            writer.append(s.toLowerCase());
            writer.append(COMMA);
        }
        writer.append("RATING");
        writer.append(NEWLINE);


        //To extract frequenct count from each of the review data.

        List<LeafReaderContext> leafContexts = reader.getContext().reader().leaves();
        for(int i=0;i<leafContexts.size();i++){
            LeafReaderContext leafContext=leafContexts.get(i);
            int startDoc=leafContext.docBase;
            int numberofDoc=leafContext.reader().numDocs();
            for(int docId=0;docId<numberofDoc;docId++){
                Document doc=leafContext.reader().document(docId);
                List<Integer> feats=new ArrayList<Integer>();
                writer.append(doc.get("REVIEWID"));
                writer.append(COMMA);
                for(String s:features){
                    writer.append(String.valueOf(termfreq(s,leafContext,startDoc,startDoc+docId)));
                    writer.append(COMMA);
                }
                writer.append(doc.get("STARS"));
                writer.append(NEWLINE);
            }
        }
        writer.close();
        System.out.print("DONE");
    }
}
