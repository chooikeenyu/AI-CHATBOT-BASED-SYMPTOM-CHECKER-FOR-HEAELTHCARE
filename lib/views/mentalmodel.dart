class MentalModel{
  String? name;
  String? definition;
  List<String>? type;
  List<String>? causes;
  List<String>? symptoms;
  List<String>? treatment;
  String? image;

  MentalModel(
    {
    this.name,
      this.definition,
      this.type,
      this.causes,
      this.symptoms,
      this.treatment,
      this.image
    });

  MentalModel.fromJson(Map<String, dynamic> json)
  {
    name = json['name'];
    definition = json['what'];
    type = json['type'];
    causes = json['causes'];
    symptoms = json['symptoms'];
    treatment = json['treatment'];
    image = json['image'];
  }
}