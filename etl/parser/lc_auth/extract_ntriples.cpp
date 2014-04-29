#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_set>
#include <boost/iostreams/filtering_stream.hpp>
#include <boost/iostreams/filter/gzip.hpp>

using namespace std;

static const char *initial_items[] = {
    "<http://www.loc.gov/mads/rdf/v1#HierarchicalGeographic>",
    "<http://www.loc.gov/mads/rdf/v1#Geographic>",
    "<http://www.loc.gov/mads/rdf/v1#Region>",
    "<http://www.loc.gov/mads/rdf/v1#CitySection>",
    "<http://www.loc.gov/mads/rdf/v1#City>",
    "<http://www.loc.gov/mads/rdf/v1#State>",
    "<http://www.loc.gov/mads/rdf/v1#County>",
    "<http://www.loc.gov/mads/rdf/v1#Country>",
    "<http://www.loc.gov/mads/rdf/v1#Territory>",
    "<http://www.loc.gov/mads/rdf/v1#Continent>",
    "<http://www.loc.gov/mads/rdf/v1#Area>",
    "<http://www.loc.gov/mads/rdf/v1#Island>",
    "<http://www.loc.gov/mads/rdf/v1#Province>",
    NULL
};

int main(int argc, char **argv){
    int last_round = 0, current_round = 0;
    int pass = 0;
    unordered_set<string> *old_items = new unordered_set<string>,
                          *current_items = new unordered_set<string>;
    while (true) {
        unordered_set<string> *new_items = new unordered_set<string>;
        if (pass == 0) {
            for (int n = 0; initial_items[n]; n++) {
                string item(initial_items[n]);
                current_items->insert(item);
                cerr << "searching for: " << item << "\n";
            }
        }
        ifstream file(argv[1], ios_base::in | ios_base::binary);
        boost::iostreams::filtering_istream infile;
        infile.push(boost::iostreams::gzip_decompressor());
        infile.push(file);
        string line;
        int lines_read = 0;
        while (getline(infile, line)) {
            if (++lines_read % 100000 == 0)
                cerr << "\r" << "pass " << pass << ": read=" << lines_read << " "
                    << "old_items=" << old_items->size() << " "
                    << "current_items=" << current_items->size() << " "
                    << "new_items=" << new_items->size();
            unordered_set<string>::const_iterator got;
            string subject, predicate, object;
            stringstream ss(line);
            ss >> subject; ss >> predicate; ss >> object;
            //cerr << subject << " " << predicate << " " << object << "\n";
            // NOTE: these subject relationships hasNarrowerAuthority and hasBroaderAuthority
            //       are blowing out the tree -- so ignore them
            if (predicate.find("Authority>") != string::npos) continue;
            if (pass) {
                if (current_items->find(subject) != current_items->end()) {
                    cout << line << "\n";
                    if (old_items->find(object) == old_items->end()) {
                        new_items->insert(object);
                        old_items->insert(object);
                        current_round++;
                    }
                }
            } else {
                if (current_items->find(object) != current_items->end()) {
                    cout << line << "\n";
                    new_items->insert(subject);
                    old_items->insert(subject);
                    current_round++;
                }
            }
        }
        cerr << "\r" << "pass " << pass << ": read=" << lines_read << " "
            << "old_items=" << old_items->size() << " "
            << "current_items=" << current_items->size() << " "
            << "new_items=" << new_items->size();
        if (current_round) {
            cerr << "\n";
            last_round = current_round;
            current_round = 0;
            pass++;
            delete current_items;
            current_items = new_items;
        } else {
            cerr << "... done.\n";
            break;
        }
    }
    return 0;
}
